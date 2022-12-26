const place = document.getElementById("place-name");
const forecast = document.getElementById("weather");
const temp = document.getElementById("temp__txt");
const humidity = document.getElementById("humidity__txt");
const feels_like = document.getElementById("feels-like");
const forecast_div = document.getElementById("forecast");
const err_div = document.getElementById("error");
const date_time = document.getElementById("date-time");
const timeUpdated = document.getElementById("time_updated");
const month_array = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const day_array = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

// Getting date
const date = new Date();
const day = date.getDate();
const month = month_array[date.getMonth()];
const weekDay = day_array[date.getDay()];


forecast_div.style.display = "none";


function getTime(unixTimestamp){
 let date = new Date(unixTimestamp * 1000);
 return date.toLocaleTimeString("en-US");

}


place.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    date_time.textContent = `${weekDay}, ${day} ${month}`;
    err_div.classList.add("hidden");
    forecast_div.classList.remove("forecast"); // reset animation
    void forecast_div.offsetWidth; // trigger reflow
    forecast_div.classList.add("forecast"); // start animation

    console.log(place.value);

    fetch(`https://127.0.0.1:8080?city=${place.value}`)
      .then((res) => {
        console.log(res.headers)
        return res.json();
      })
      .then((data) => {


        console.log(data)
        //checking for error message returned by exception
        if (data.error) {
            forecast.textContent = "We're unable to fetch the weather at the moment, please try again."
            temp.textContent = ``;
            humidity.textContent = ``;
            feels_like.textContent = ``;
            forecast_div.style.display = "block";
            timeUpdated.style.display = "none";
        } 
        else if(data.rate_limit_response){
          forecast.textContent =
            data.rate_limit_response,
          temp.textContent = ``;
          humidity.textContent = ``;
          feels_like.textContent = ``;
          forecast_div.style.display = "block";
          timeUpdated.style.display = "none";
        }
        else {
          forecast.textContent = data.weather;
          temp.textContent = `${Math.floor(data.temp)}℃`;
          humidity.textContent = `Humidity: ${data.humidity}%`;
          feels_like.textContent = `Feels like ${Math.floor(data.feels_like)}℃`;
          forecast_div.style.display = "block";
          timeUpdated.style.display = "block";
          timeUpdated.innerHTML = `<p>This data was last refreshed at ${getTime(data.time_refreshed)} and will next be updated at ${getTime(data.next_refresh)}.</p>`;
        }
      })
      .catch((err) => {
        console.log(err);
        err_div.classList.remove("hidden");
        forecast_div.style.display = "none";
      });
  }
});
