import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crimes.models import CrimeData

from prophet import Prophet
import pandas as pd

@csrf_exempt
def crimes(request):
    if request.method == "GET":
        state = request.GET.get('state')
        crime_type = request.GET.get('crime_type')
        
        if not state:
            return JsonResponse({"success": False, "message": "State parameter is required"}, status=400)

        queryset = CrimeData.objects.filter(state__iexact=state)

        if crime_type:
            valid_fields = [field.name for field in CrimeData._meta.fields if field.name not in ['id', 'state', 'year']]
            if crime_type.lower() in valid_fields:
                queryset = queryset.values('year', crime_type)
                return JsonResponse(list(queryset), safe=False, status=200)
            else:
                return JsonResponse({"success": False, "message": f"Invalid crime_type. Choose from {valid_fields}"}, status=400)

        data = list(queryset.values())
        return JsonResponse({"success": True, "message": "Data fetched successfully", "data": data}, safe=False, status=200)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def predictions(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "message": "Only POST method allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"success": False, "message": "Invalid JSON payload"}, status=400)

    forecast_years = 10

    def predict_for_field(df, crime_field):
        try:
            df['year'] = df['year'].astype(int)
        except Exception:
            raise ValueError("The 'year' field must be convertible to integer.")
        df = df.sort_values('year')
        df['ds'] = pd.to_datetime(df['year'].astype(str) + '-01-01')
        df['y'] = pd.to_numeric(df[crime_field], errors='coerce')
        df = df[['ds', 'y']].dropna()
        if df.shape[0] < 3:
            raise ValueError(f"Not enough data points to predict {crime_field}.")
        model = Prophet(yearly_seasonality=False, daily_seasonality=False, weekly_seasonality=False)
        model.fit(df)
        last_year = df['ds'].dt.year.max()
        future_dates = pd.date_range(start=f'{last_year + 1}-01-01', periods=forecast_years, freq='YE')
        future = pd.DataFrame({'ds': future_dates})
        forecast = model.predict(future)
        forecast['year'] = forecast['ds'].dt.year
        return forecast[['year', 'yhat']].to_dict(orient='records')

    if isinstance(payload, list):
        historical_data = payload
        if not historical_data:
            return JsonResponse({"success": False, "message": "Empty data array."}, status=400)
        first_record = historical_data[0]
        if not isinstance(first_record, dict):
            return JsonResponse({"success": False, "message": "Records must be JSON objects."}, status=400)
        if 'year' not in first_record:
            return JsonResponse({"success": False, "message": "Each record must contain a 'year' field."}, status=400)
        crime_fields = [k for k in first_record.keys() if k != 'year']
        if len(crime_fields) != 1:
            return JsonResponse({"success": False, "message": "For specific crime type data, each record must have exactly one crime field besides 'year'."}, status=400)
        crime_field = crime_fields[0]
        df = pd.DataFrame(historical_data)
        try:
            predictions = predict_for_field(df, crime_field)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
        return JsonResponse({"success": True, "message": "Predictions fetched successfully", "data": predictions}, safe=False)

    elif isinstance(payload, dict) and "data" in payload:
        records = payload["data"]
        if not isinstance(records, list) or not records:
            return JsonResponse({"success": False, "message": "The 'data' key must contain a non-empty list of records."}, status=400)
        df = pd.DataFrame(records)
        if 'year' not in df.columns:
            return JsonResponse({"success": False, "message": "Records must include a 'year' column."}, status=400)
        excluded = {'id', 'state', 'year'}
        crime_fields = [col for col in df.columns if col not in excluded]
        predictions_all = {}
        errors = {}
        for field in crime_fields:
            try:
                temp_df = df[['year', field]].copy()
                predictions_all[field] = predict_for_field(temp_df, field)
            except Exception as e:
                errors[field] = str(e)
        response = {
            "success": True,
            "message": "Predictions fetched successfully",
            "data": predictions_all
        }
        if errors:
            response["errors"] = errors
        return JsonResponse(response, safe=False)

    else:
        return JsonResponse({"success": False, "message": "Invalid payload format. Provide either a JSON array or an object with a 'data' key."}, status=400)