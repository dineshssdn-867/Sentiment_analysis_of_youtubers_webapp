"use strict";{function ready(e){"loading"!==document.readyState?e():document.addEventListener("DOMContentLoaded",e)}ready(function(){function e(e){e.preventDefault(),new URLSearchParams(window.location.search).has("_popup")?window.close():window.history.back()}document.querySelectorAll(".cancel-link").forEach(function(n){n.addEventListener("click",e)})})}