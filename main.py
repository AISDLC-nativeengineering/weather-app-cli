import click
import httpx

WTTR_URL = "https://wttr.in/{city}?format=j1"

@click.command()
@click.argument("city")
def fetch_weather(city):
    """Fetch and display weather for CITY using wttr.in API."""
    url = WTTR_URL.format(city=city)

    try:
        resp = httpx.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # wttr.in returns weather for the nearest location as 'current_condition' key
        cc = data.get("current_condition", [{}])[0]
        if not cc:
            raise ValueError("Weather data not found for this city.")
        temp_c = cc.get("temp_C", "N/A")
        cond = cc.get("weatherDesc", [{}])[0].get("value", "N/A")
        humidity = cc.get("humidity", "N/A")
        click.echo(f"Weather for {city}:")
        click.echo(f"Temperature: {temp_c} °C")
        click.echo(f"Condition: {cond}")
        click.echo(f"Humidity: {humidity}%")
    except httpx.RequestError:
        click.secho("Network error. Unable to reach wttr.in API.", fg="red")
    except httpx.HTTPStatusError:
        click.secho("Failed to fetch weather. City may be incorrect or unavailable.", fg="yellow")
    except Exception as ex:
        click.secho(f"Error: {ex}", fg="red")

if __name__ == "__main__":
    fetch_weather()
