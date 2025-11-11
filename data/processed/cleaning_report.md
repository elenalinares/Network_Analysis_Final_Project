# Cleaning report (2025-11-11T17:16:53.134966+00:00)
## Summary counts
- Raw airports rows: 9075
- Cleaned airports rows: 9075
- Airport duplicate-ID rows removed: 0
- Airport invalid-coord rows removed: 0
- Raw routes rows: 92695
- Routes dropped (missing departure/destination): 99
- Routes removed (invalid airport references): 90
- Routes self-loops removed: 4
- Cleaned routes rows: 92502
- Unique route pairs (weighted): 50168
## Examples of removed route rows (invalid airport refs)
- {'Airline ID': 'AA', 'Departure': 'KSWO', 'Destination': 'DFW'}
- {'Airline ID': 'AA', 'Departure': 'DFW', 'Destination': 'KSWO'}
- {'Airline ID': 'LA', 'Departure': 'LIM', 'Destination': 'SPJJ'}
- {'Airline ID': 'LA', 'Departure': 'SPJJ', 'Destination': 'LIM'}
- {'Airline ID': 'LA', 'Departure': 'SPJB', 'Destination': 'LIM'}
- {'Airline ID': 'LA', 'Departure': 'LIM', 'Destination': 'SPJB'}
- {'Airline ID': 'LA', 'Departure': 'TRU', 'Destination': 'SPJB'}
- {'Airline ID': 'LA', 'Departure': 'SBAE', 'Destination': 'GRU'}
- {'Airline ID': 'LA', 'Departure': 'GRU', 'Destination': 'SBAE'}
- {'Airline ID': 'LA', 'Departure': 'SCL', 'Destination': 'SCRG'}

## Examples of removed self-loop rows
- {'Airline ID': 'IL', 'Departure': 'PKN', 'Destination': 'PKN'}
- {'Airline ID': 'MF', 'Departure': 'HGH', 'Destination': 'HGH'}
- {'Airline ID': 'PB', 'Departure': 'YYT', 'Destination': 'YYT'}
- {'Airline ID': 'W6', 'Departure': 'LWO', 'Destination': 'LWO'}
