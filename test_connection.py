# Connection Test
import pyvisa

rm = pyvisa.ResourceManager()

#rm.list_resources()

my_instrument = rm.open_resource('TCPIP::192.168.1.55::INSTR')

def test_connection():
    assert my_instrument.query('*IDN?') == "RIGOL TECHNOLOGIES,MSO8104,DS8A222300220,00.01.02.00.02\n"

if __name__ == "__main__":
    test_connection()