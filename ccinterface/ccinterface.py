import time
import smbus


class CCInterface:
    
    ADDRESS = None
    bus = None

    def __init__(self,addr,  bus_):
        self.ADDRESS=addr
        self.bus = bus_

    def read_16_bit_val(self, addr):
        val = self.bus.read_byte_data(self.ADDRESS,addr)
        val *= 256
        val += self.bus.read_byte_data(self.ADDRESS, addr+1)
        return val

    def write_16_bit_val(self, addr, val):
        (olderbyte, youngerbyte) = val.to_bytes(2, byteorder="big")
        self.bus.write_byte_data(self.ADDRESS,addr, olderbyte)
        self.bus.write_byte_data(self.ADDRESS, addr + 1, youngerbyte)      

    def set_current(self, val):
        ''' sets "set" current for internal regulator '''
        if (val < 0.0 or val > 2.0):
            print("bad current value")
            return
        raw_val =int( (val / 3.3) * 4096)
        self.write_16_bit_val( 1, raw_val)
        self.bus.write_byte_data( self.ADDRESS, 3, 0x01) # confirm funushing sending data.

    def get_set_current(self):
        val = int(self.read_16_bit_val(1))
        return (val /4096) *3.3

    def get_output_val(self):
        ''' gets output pwm val '''
        return self.bus.read_byte_data(self.ADDRESS, 0)

    def get_input_val(self):
        ''' this method gets reading from analog voltage sensor '''
        val = self.read_16_bit_val(4)
        return (val / 4096) * 3.3

    def enable_regulator(self):
        ''' sets val whutch enables internal regulator '''
        self.bus.write_byte_data(self.ADDRESS, 6, 0x01)

    def disable_regulator(self):
        ''' sets val whitch disables internal regulator '''
        self.bus.write_byte_data(self.ADDRESS, 6, 0x00)

    def get_mode(self):
        '''gets current setting'''
        return self.bus.read_byte_data(self.ADDRESS, 6)

    def print_status(self):
        ''' prints all cc board values '''
        output_val = self.get_output_val()
        real_current = self.get_input_val()
        set_current = self.get_set_current()
        mode = self.get_mode()
        print("Board no:", self.ADDRESS, " mode: ", mode )
        print("PWM val: ", output_val)
        print("Set curr:", set_current, "Real curr", real_current)

if __name__ == '__main__':
    print("ConstantCurrent Interface INIT")
    CCI = CCInterface(0x20, smbus.SMBus(1))
    CCI.print_status()
    
