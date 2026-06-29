# Description

Parse Flipper Zero `.sub` files for transmission from a CC1101 radio connected to a Raspberry Pi with `python-cc1101`.

# Setup

Install [python-cc1101](https://github.com/fphammerle/python-cc1101) with

```bash
pip3 install --user --upgrade cc1101
```

Connect your CC1101 to your Raspberry Pi according to the following table, copied from the link above:

| CC1101 | Raspberry Pi                                                                                                                                                                                                                                                                                        |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VDD    | 3.3V (Pin 1 or 17)                                                                                                                                                                                                                                                                                  |
| SI     | MOSI (Pin 19)                                                                                                                                                                                                                                                                                       |
| SO     | MISO (Pin 21)                                                                                                                                                                                                                                                                                       |
| CSn    | CE0 (Pin 24)                                                                                                                                                                                                                                                                                        |
| SCLK   | SCLK (Pin 23)                                                                                                                                                                                                                                                                                       |
| GDO2\* | Any GPIO pin, commonly GPIO25 (Pin 22) \[[1](https://github.com/SpaceTeddy/CC1101/blob/0d0f011d3b808e36ad57fab596ed5e1db9516856/README.md#hardware-connection),[2](https://allgeek.de/2017/07/31/cc1101-spi-raspberry-adapter-fuer-homegear-homematicmax/),[3](https://securipi.co.uk/cc1101.pdf)\] |
| GDO0\* | Any GPIO pin, GPIO24 (Pin 18) recommended                                                                                                                                                                                                                                                           |
| GND    | Ground                                                                                                                                                                                                                                                                                              |

Be sure that `dtparam=spi=on` appears uncommented in `/boot/firmware/config.txt` on your Raspberry Pi.

# Usage

```
python py-sub-tx [-h|--help] [(-r|--reps) REPS] files [...]
```

where `REPS` is the number of times each signal should be repeated.

# Limitations

Currently only RAW and EV1527 ("Princeton") formats are supported.
