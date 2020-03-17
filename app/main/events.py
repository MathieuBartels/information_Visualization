from flask_socketio import emit, send
from .. import socketio
from . import routes
from .. import data

@socketio.on("model_update")
def on_model_update(info):
    """Updating model due to change in data"""
    print("Emitting model update")
    new_value = info['newValue']
    column = info['column']
    row = info['row']
    # data.update_data(area, var, new_value)
    data.update_data(row, column, new_value)

@socketio.on("active_update")
def on_active_update(info):
    """Updating active sliders due to change in data"""
    print("Emitting active update")
    actives = list(info['slider_names'])
    values = list(info['values']) 
    data.update_active(actives, values)

@socketio.on("active_update_view2")
def on_active_update(info):
    """Updating active sliders due to change in data"""
    print("Emitting active update")
    actives = list(info['slider_names'])
    values = list(info['values']) 
    data.update_active_view2(actives, values)

@socketio.on("slider_value_update")
def on_slider_update(info):
    """Updating active sliders due to change in data"""
    print("Emitting active slider value")
    slider_name = info['slider_name']
    var = float(info['var'])
    df = data.update_slider_value(slider_name, var)
    emit('rank_update', {'rank': df.to_numpy().tolist()})

@socketio.on("dataframe_update")
def update_dataframe(info):
    image_name = info['image_name']
    slider_name = info['slider_name']
    new_value = info['value']

    print('updating ', image_name, slider_name, new_value)

    data.update_data(image_name[0], slider_name, new_value)



@socketio.on("slider_value_update_view2")
def on_slider_update_view2(info):
    """Updating active sliders due to change in data"""
    print("Emitting active slider value")
    slider_name = info['slider_name']
    var = float(info['var'])
    image_name = info['image_name']
    df = data.update_slider_value_view2(slider_name, var, image_name)
    emit('rank_update', {'rank': df.to_numpy().tolist()})


@socketio.on('connect')
def test_connect():
    print("Connection succesful")
    