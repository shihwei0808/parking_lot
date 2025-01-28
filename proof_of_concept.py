import easyocr
from datetime import datetime
from datetime import timezone
from datetime import timedelta

reader = easyocr.Reader(['en'],gpu=False)
parked_Vehicles = dict()
def parking_lot_ocr(img_path:str,ntd_per_sec:int=1):
    results = reader.readtext(img_path,detail=0)
    entry_time = datetime.now(timezone.utc)+timedelta(hours=8)
    entry_time_str = entry_time.strftime('%Y-%m-%d %H:%M:%S')
    car_plate = results[0]
    if car_plate not in parked_Vehicles.keys():
       parked_Vehicles[car_plate] = entry_time
       print(f'歡迎來到停車場{car_plate}!')
       print(f'您的進場時間是 : {entry_time_str}.')
       print(f'停車費是以一秒 NT${ntd_per_sec}計算.')
    else:
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_Vehicles[car_plate]
        second_elapsed = int(time_elapsed.total_seconds())
        charge_amount = second_elapsed * ntd_per_sec
        print(f'bye bye bye {car_plate}!')
        print(f'您總共待了 {second_elapsed}秒.')
        print(f'停車費用是 NT${charge_amount:,}.')
        parked_Vehicles.pop(car_plate,None)
parking_lot_ocr("data/car_plate_1.jpg")
print(parked_Vehicles)
parking_lot_ocr("data/car_plate_1.jpg")
print(parked_Vehicles)