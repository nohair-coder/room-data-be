# import requests
#
# baseURL = 'http://localhost:8000/'
#
# try:
#
#     json_object = {'build_unit_station': '01-01-0001', 'status_num': '00000', 'status': 'on'}
#
#     r = requests.patch(baseURL + 'station/' + '1' + '/', data=json_object)
#     # ack = json.loads(r.text)
#     print('devicePut ackackackackack', r.status_code)
# except:
#     print('devicePut connect failed !')
#
import time
a = time.strftime("%Y-%m-%d %H:%M", time.strptime('202011241050', "%Y%m%d%H%M"))
print(a)

