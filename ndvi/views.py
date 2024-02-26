from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ndvi
from .serializers import NdviSerializer
from typing import Dict, Any
from datetime import datetime
import csv
from django.http import HttpResponse

from .ndvi_calculation import chart

class NdviViewSet(viewsets.ModelViewSet):
    queryset = Ndvi.objects.all()
    serializer_class = NdviSerializer
    
    def create(self, request, *args, **kwargs):
        # Perform the calculation here
        title = request.data.get('title')
        polygon = request.data.get('polygon')
        
        # Calculate NDVI
        cvs_data = self.calculate_ndvi(title, polygon)
        
        print(f"Calculate cvs_data: {cvs_data}")
        
        # Perform your calculation logic here, for example:
        # ndvi_value = 42.0  # Replace this with your actual calculation
        
        # Create a new Ndvi instance with the calculated value
        ndvi = Ndvi.objects.create(
            title=title,
            polygon=polygon,
            cvs_data = cvs_data,
            ndvi=34.0  # Assuming 'ndvi' is the field to store the calculation result
        )
        
        # Serialize the new instance
        serializer = self.get_serializer(ndvi)
        
        #  # Calculate duration
        # duration = request.end_date - request.start_time
        # print(f"Request duration: {duration} seconds")
        
        # Return a successful response with the serialized data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def calculate_ndvi(self, title: str, polygon: Dict[str, Any]) -> float:
        print(f"title: {title} polygon: {polygon}")

        # Call the ndvi_gen function to calculate NDVI
        ndvi_value = chart(polygon['coordinates'][0], 400, "2017-02-25", "2020-02-25")
        
        # print(f"NDVI value: {ndvi_value}")
        
        # # Create CSV rows
        # rows = [['Date', 'NDVI']]
        # for feature in ndvi_value:
        #     # rows.append([feature['properties']['date'], feature['properties']['ndvi']])
        #     if 'ndvi' in feature['properties']:
        #         rows.append([feature['properties']['date'], feature['properties']['ndvi']])
        
        # Create CSV rows
        rows = [['Date', 'NDVI']]
        for feature in ndvi_value:
            if 'ndvi' in feature['properties']:
                date = feature['properties']['date']
                ndvi = feature['properties']['ndvi']
                rows.append([date, ndvi])

        # Convert rows to CSV string
        csv_data = '\n'.join([','.join(map(str, row)) for row in rows])

        # print(f"rows: {csv_data}")
        
        #   # Create the HttpResponse object with the appropriate CSV content
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="ndvi_data.csv"'

        # # Write CSV rows to the response
        # writer = csv.writer(response)
        # for row in rows:
        #     writer.writerow(row)

        # # Return the CSV response
        # print(f"response: {response}")

        return csv_data
    