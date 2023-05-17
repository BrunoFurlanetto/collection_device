# Reaction Time Collection Device

This is a design of a simple and choice reaction time collection device,
that uses visual, sound and auditory stimuli. The project is based on the library
microPython and is designed to work with the ESP32 microcontroller.

## Functionalities

The reaction time collection device allows you to measure the reaction time of a
user in response to different stimuli. It provides three types of stimuli:
visual, sound and auditory. The user must react as quickly as possible
when the stimulus is presented and the device records the reaction time.

## Prerequisites

- ESP32 microcontroller
- Connection to computer for programming
- Python environment with microPython installed
- Internet access to download dependencies

## Installation

1. Clone this repository on your local machine:

    ```
    git clone https://github.com/BrunoFurlanetto/collection_device.git
    ```

2. Access the project directory:

    ```
    cd device-collection-time-reaction
    ```

3. Create a virtual environment using the `venv` tool:

    ```
    python -m venv venv
    ```

4. Activate the virtual environment:

     - On Windows:

       ```
       venv\Scripts\activate.bat
       ```

     - On Linux/macOS:

       ```
       source venv/bin/activate
       ```

5. Install the project's dependencies:

    ```
    pip install -r requirements.txt
    ```

6. Clear the ESP32 flash:

     - Connect the ESP32 to the computer via USB. Make sure the USB cable also has
        data transmission capability.
     - Open a terminal and run the following command:

       ```
       esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
       ```

       **Note:** Replace `/dev/ttyUSB0` with the proper serial port path
       ESP32 on your system.

## Usage

1. Connect the ESP32 to the computer via USB.

2. Make sure the virtual environment is enabled:

     - On Windows:

       ```
       venv\Scripts\activate.bat
       ```

     - On Linux/macOS:

       ```
       source venv/bin/activate
       ```

3. Run the main program and provide the communication port with the ESP32:

    ```
    python main.py
    ```

4. Follow the instructions on the terminal to interact with the time collection device
    of reaction.

5. To get the test output files, run the `get_file.bat` file
     for windows and `get_file.sh` on linux. Then provide the name you want for the
     files.

## License

This project is licensed under the [MIT License](LICENSE).