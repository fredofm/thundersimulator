# Thunderstorm simulator

This project is based on Micropython and adapted to work on a Raspberry Pico W microcontroller.

## Secrets

I'm using ujson library to get my secrets from a json file. To get this example working place a *secrets.json* file at the root directory with the following structure:

```json
{
	"wifi": {
		"ssid": "YOUR SSID",
		"pass": "YOUR PASSWORD"
	}
}
```

## Run

Upload your code to the Rasberry Pico micro-controller using using [Thonny](https://thonny.org/) or similar tool that can connect to the micro-controller using [RELP](https://codewith.mu/en/tutorials/1.1/repl).