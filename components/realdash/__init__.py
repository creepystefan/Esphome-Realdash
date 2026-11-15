import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, binary_sensor, sensor, text_sensor, number
from esphome.const import (
    CONF_BINARY_SENSORS,
    CONF_ID,
    CONF_NAME,
    CONF_SENSORS,
    CONF_BINARY_SENSORS,
    CONF_TEXT_SENSORS,
    
)


CONF_CANID = 'canid'
CONF_ID2 = 'id2'
CONF_NUMBERS = "numbers"

DEPENDENCIES = ["uart"]
CODEOWNERS = ["@creepystefan"]


realdash_ns = cg.esphome_ns.namespace("realdash")
Realdash = realdash_ns.class_("Realdash", cg.Component, uart.UARTDevice)
RealdashDevice = realdash_ns.class_("RealdashDevice")


CONFIG_SENSORS_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(sensor.Sensor),
        cv.Optional(CONF_ID2): cv.use_id(sensor.Sensor),
        cv.Required(CONF_CANID): cv.int_range(min=1, max=0xFFFFFFFF),
    }
)

CONFIG_BINARY_SENSORS_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(binary_sensor.BinarySensor),
        cv.Required(CONF_CANID): cv.int_range(min=1, max=0xFFFFFFFF),
    }
)

CONFIG_TEXT_SENSORS_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(sensor.Sensor),
        cv.Required(CONF_CANID): cv.int_range(min=1, max=0xFFFFFFFF),
    }
)

CONFIG_NUMBERS_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(number.Number),
        cv.Optional(CONF_ID2): cv.use_id(number.Number),
        cv.Required(CONF_CANID): cv.int_range(min=1, max=0xFFFFFFFF),
    }
)



CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Realdash),
        cv.Optional(CONF_SENSORS): cv.ensure_list(CONFIG_SENSORS_SCHEMA),
        cv.Optional(CONF_BINARY_SENSORS): cv.ensure_list(CONFIG_BINARY_SENSORS_SCHEMA),
        cv.Optional(CONF_TEXT_SENSORS): cv.ensure_list(CONFIG_TEXT_SENSORS_SCHEMA),
        cv.Optional(CONF_NUMBERS): cv.ensure_list(CONFIG_NUMBERS_SCHEMA),
    }
).extend(uart.UART_DEVICE_SCHEMA)




async def to_code(config):
   var = cg.new_Pvariable(config[CONF_ID])
   await cg.register_component(var, config)
   await uart.register_uart_device(var, config)

   for sensor_cfg in config.get(CONF_SENSORS, []):
        s = await cg.get_variable(sensor_cfg[CONF_ID])
        if CONF_ID2 in sensor_cfg:
            s2 = await cg.get_variable(sensor_cfg[CONF_ID2])
            cg.add(var.register_sensor(sensor_cfg[CONF_CANID], s, s2))
        if CONF_ID2 not in sensor_cfg:
            cg.add(var.register_sensor(sensor_cfg[CONF_CANID], s))
        
    
   for sensor_cfg in config.get(CONF_BINARY_SENSORS, []):
        s = await cg.get_variable(sensor_cfg[CONF_ID])
        cg.add(var.register_binary_sensor(sensor_cfg[CONF_CANID], s))

   for text_sensor_cfg in config.get(CONF_TEXT_SENSORS, []):
        s = await cg.get_variable(sensor_cfg[CONF_ID])
        cg.add(var.register_text_sensor(sensor_cfg[CONF_CANID], s))

   for sensor_cfg in config.get(CONF_NUMBERS, []):
        s = await cg.get_variable(sensor_cfg[CONF_ID])
        if CONF_ID2 in sensor_cfg:
            s2 = await cg.get_variable(sensor_cfg[CONF_ID2])
            cg.add(var.register_number(sensor_cfg[CONF_CANID], s, s2))
        if CONF_ID2 not in sensor_cfg:
            cg.add(var.register_number(sensor_cfg[CONF_CANID], s))
    
      
async def register_realdash_device(var, config):
    parent = await cg.get_variable(config[CONF_REALDASH_ID])
    cg.add(var.set_parent(parent))


 
