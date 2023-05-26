# Spot-Hinta.fi Data to Discord

This Python script retrieves electricity price information from the Spot-Hinta.fi API and sends it to a Discord channel using a webhook. It provides the price per kilowatt-hour (kWh) with and without tax information.

## Prerequisites

- Python 3.x
- `requests` library (install using `pip install requests`)

## Configuration

Before running the script, make sure to set up the necessary configuration:

1. Create a Discord webhook in your Discord server/channel. Refer to the Discord documentation for instructions on creating a webhook: [Creating a Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

2. Set the Discord webhook URL as an environment variable named `DISCORD_WEBHOOK_URL`. The script will retrieve this URL from the environment variables using `os.environ.get('DISCORD_WEBHOOK_URL')`.

## Usage

1. Clone the repository or download the script file.

2. Install the required dependencies by running the following command:
pip install requests


3. Set the `DISCORD_WEBHOOK_URL` environment variable to the Discord webhook URL.

4. Run the script using the following command:
python main.py


5. The script will make an HTTP call to the Spot-Hinta.fi API to retrieve the electricity price information. If the call is successful (status code 200), the script will format the data and send it to the Discord channel specified by the webhook URL.

6. The script will run indefinitely, waiting for the next full hour and then making the HTTP call again to update the price information.

Note: Make sure to keep the Discord webhook URL confidential and do not commit it to version control.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

