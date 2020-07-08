import RPi.GPIO as GPIO

class LedUserInterface:

    def __init__(self, log_button_handler):
        self._log_button_gpio_number = 24
        self._log_led_gpio_number = 25
        self._connection_led_gpio_number = 23
        GPIO.setmode(GPIO.BCM)
        self._setup_log_button(log_button_handler)
        self._setup_log_led()
        self._setup_connection_led()

    def __del__(self):
        GPIO.cleanup()

    def _setup_log_button(self, log_button_handler):
        GPIO.setup(
            self._log_button_gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self._log_button_gpio_number, 
            GPIO.FALLING, 
            callback=log_button_handler, 
            bouncetime=1000)

    def _setup_log_led(self):
        GPIO.setup(self._log_led_gpio_number, GPIO.OUT)

    def _setup_connection_led(self):
        GPIO.setup(self._connection_led_gpio_number, GPIO.OUT)

    def turn_log_led_on(self):
        GPIO.output(self._log_led_gpio_number, 1)

    def turn_log_led_off(self):
        GPIO.output(self._log_led_gpio_number, 0)

    def turn_connection_led_on(self):
        GPIO.output(self._connection_led_gpio_number, 1)

    def turn_connection_led_off(self):
        GPIO.output(self._connection_led_gpio_number, 0)
