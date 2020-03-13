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
    actives = list(info['actives'])
    data.update_active(actives)

@socketio.on("slider_value_update")
def on_active_update(info):
    """Updating active sliders due to change in data"""
    print("Emitting active slider value")
    slider_name = info['slider_name']
    var = float(info['var'])
    data.update_slider_value(slider_name, var)



@socketio.on('connect')
def test_connect():
    print("Connection succesful")
    