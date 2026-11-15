#pragma once

#include <vector>

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/core/defines.h"

#ifdef USE_SENSOR
#include "esphome/components/sensor/sensor.h"
#endif

#ifdef USE_BINARY_SENSOR
#include "esphome/components/binary_sensor/binary_sensor.h"
#endif

#ifdef USE_TEXT_SENSOR
#include "esphome/components/text_sensor/text_sensor.h"
#endif

#ifdef USE_NUMBER
#include "esphome/components/number/number.h"
#endif

#ifdef USE_LOGGER
#include "esphome/components/logger/logger.h"
#endif


namespace esphome::realdash {
 
 class RealdashDevice;

class Realdash : public uart::UARTDevice, public Component {
 public:
 
 Realdash() = default;

#ifdef USE_SENSOR
  void register_sensor(uint32_t canid, esphome::sensor::Sensor *sensor, esphome::sensor::Sensor *sensor2 = nullptr);
#endif

#ifdef USE_BINARY_SENSOR
  void register_binary_sensor(uint32_t canid, esphome::binary_sensor::BinarySensor *binary_sensor);
#endif

#ifdef USE_TEXT_SENSOR
  void register_text_sensor(uint32_t canid, esphome::text_sensor::TextSensor *text_sensor);
#endif

#ifdef USE_NUMBER
  void register_number(uint32_t canid, esphome::number::Number *number, esphome::number::Number *number2 = nullptr); 
#endif


float get_setup_priority() const override;
void register_device(RealdashDevice *device) { this->devices_.push_back(device); }
void setup() override;
void loop() override;
void dump_config() override;
void send44(uint32_t canid_, uint32_t data1, uint32_t data2 );
void send66(uint32_t canid_, uint8_t size_identifier, const uint8_t *payload, size_t payload_len);
void send_text(uint32_t canid_);
void send_data(const uint8_t *data, uint8_t len);
void can_speed(uint8_t can_speed);
void can_mode(uint8_t can_mode);

 private:
  uint32_t canid_;

  //using number_type_t = enum { TYPE_NUMBER };
  using sensor_type_t = enum { TYPE_SENSOR, TYPE_BINARY_SENSOR, TYPE_TEXT_SENSOR, TYPE_NUMBER };
    using sensors_t = struct {
    
    uint32_t canid;
    sensor_type_t type;
    
  #ifdef USE_SENSOR
      esphome::sensor::Sensor *sensor;
      esphome::sensor::Sensor *sensor2;
  #endif

  #ifdef USE_BINARY_SENSOR
      esphome::binary_sensor::BinarySensor *binary_sensor;
  #endif

  #ifdef USE_TEXT_SENSOR
      esphome::text_sensor::TextSensor *text_sensor;
  #endif

  #ifdef USE_NUMBER
      esphome::number::Number *number;
      esphome::number::Number *number2;
  #endif
    
};
/*
  using numbers_t = struct {
    
    uint32_t canid;
    number_type_t type;
    
  #ifdef USE_NUMBER
      esphome::number::Number *number;
  #endif
    
};
*/
  std::vector<sensors_t> sensors_;
  //std::vector<numbers_t> numbers_;
  

  protected:
   std::vector<RealdashDevice *> devices_;
   uint32_t zero = 0x00;
   uint32_t state_on = 0xff000000;
   
  

};

class RealdashDevice {
 public:
  void set_parent(Realdash *parent) { parent_ = parent; }
  
  void send66(uint32_t canid_, uint8_t size_identifier, const uint8_t *payload, size_t payload_len) {
    this->parent_->send66(canid_, size_identifier, payload, payload_len); }

  void send44(uint32_t canid_, uint32_t data1 = 0, uint32_t data2 = 0) {
    this->parent_->send44(canid_, data1, data2); }

  void can_speed(uint8_t can_speed) {
    this->parent_->can_speed(can_speed); }

  void can_mode(uint8_t can_mode) {
    this->parent_->can_mode(can_mode); }

  
  

 protected:
  friend Realdash;
  Realdash *parent_;
};

}  // namespace esphome::realdash


