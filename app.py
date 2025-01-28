import gradio as gr
import easyocr
from datetime import datetime
from datetime import timedelta
from datetime import timezone

reader = easyocr.Reader(['en'],gpu=False)
parked_Vehicles = dict()
def parking_lot_ocr(uploaded_img,ntd_per_sec:int=1):
    results = reader.readtext(uploaded_img,detail=0)
    entry_time = datetime.now(timezone.utc)+timedelta(hours=8)
    entry_time_str = entry_time.strftime('%Y-%m-%d %H:%M:%S')
    car_plate = results[0]
    if car_plate not in parked_Vehicles.keys():
       parked_Vehicles[car_plate] = entry_time
       output_message = f"""
       歡迎來到停車場{car_plate}!\n
       您的進場時間是 : {entry_time_str}\n
       停車費是以一秒 NT${ntd_per_sec}計算.
       """
       return output_message
    else:
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_Vehicles[car_plate]
        second_elapsed = int(time_elapsed.total_seconds())
        charge_amount = second_elapsed * ntd_per_sec
        parked_Vehicles.pop(car_plate,None)
        output_message = f"""
        bye bye bye {car_plate}!\n
        您總共待了 {second_elapsed}秒.
        停車費用是 NT${charge_amount:,}.
        """
        return output_message

demo = gr.Interface(fn=parking_lot_ocr,
                    inputs=gr.Image(),
                    outputs="text",
                    title="小小停車場")
demo.launch()