$(document).ready(function() {
    $(".cal-div").click(function() {
        $(".cal-div").removeClass('cal-highlight')
        $(this).addClass("cal-highlight");
    });
    cal_click(today_day);
});
const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const d = new Date();
const today_day = days[d.getDay()];
const show = JSON.parse(
    document.currentScript.nextElementSibling.textContent
    );
const cal_click = (day) => {
    const video_cont = document.getElementsByClassName("video-container");
    const workout_tab  = document.getElementsByClassName("workout-tab");
    const no_video = document.getElementsByClassName("no-video");
    const complete_btn = document.getElementById("mark-complete-button");
    if(show[day][0]){
        video_cont[0].classList.remove("hidden");
        workout_tab[0].classList.remove("hidden");
        no_video[0].classList.add("hidden");
    }else{
        video_cont[0].classList.add("hidden");
        workout_tab[0].classList.add("hidden");
        no_video[0].classList.remove("hidden");
    }
    //present
    if(days.indexOf(day) == d.getDay()){
        console.log('test1')
        console.log(show[day])
        if(show[day][1]){
            complete_btn.disabled = true;
            complete_btn.innerText = "Completed";
            complete_btn.style.backgroundColor = "#C6E59C";
        }else{
            complete_btn.disabled = false;
            complete_btn.innerText = "Mark day completed";
            complete_btn.style.backgroundColor = "#A5F739";
        }
    //past
    }else if(days.indexOf(day) < d.getDay()){
        complete_btn.disabled = true;
        if(show[day][1]){
            complete_btn.innerText = "Completed";
            complete_btn.style.backgroundColor = "#C6E59C";
        }else{
            complete_btn.innerText = "Incompleted";
            complete_btn.style.backgroundColor = "#EF8986";
        }
    //future
    }else{
        complete_btn.disabled = true;
        complete_btn.innerText = "Mark day completed";
        complete_btn.style.backgroundColor = "#C6E59C";
    }
};
