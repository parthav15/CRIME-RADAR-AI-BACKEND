import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crimes.models import CrimeData

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

