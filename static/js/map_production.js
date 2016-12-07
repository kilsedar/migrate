var i=-1, intervalID, counter=6, duration, trem, submitButtonRemoved, title="", extents=[], alpha3_countries=[], alpha3_selected="", mapClickKey, mapPointerMoveKey, ELdeactivated=true;
//var alpha3_countries = ["ITA", "TUR", "POL", "UGA", "UKR"];
var questionnaire = {};
var gameResults = {};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function decrypt(string) {
  var ciphertext = CryptoJS.enc.Base64.parse(string);
  var iv = ciphertext.clone();
  iv.sigBytes = 16;
  iv.clamp();
  ciphertext.words.splice(0, 4); //delete 4 words = 16 bytes
  ciphertext.sigBytes -= 16;

  var key = CryptoJS.enc.Utf8.parse("1234567890123456");

  //decryption
  var decrypted = CryptoJS.AES.decrypt({ciphertext: ciphertext}, key, {
    iv: iv,
    mode: CryptoJS.mode.CFB
  });
  return decrypted.toString(CryptoJS.enc.Utf8);
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/*var bingAerial = new ol.layer.Tile({
  visible: true,
  source: new ol.source.BingMaps({
    key: 'AoBGjR_hL31CvYYbkiVXXbuL24a5lu1eurrynYZgh86MXNfMy9mNC6v0RG9d1CRG',
    imagerySet: 'Aerial'
  })
});*/

var osm = new ol.layer.Tile({
  source: new ol.source.OSM({
    "url" : "http://{a-c}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
  })
});

var map = new ol.Map({
  layers: [osm],
  target: document.getElementById('map'),
  controls: ol.control.defaults().extend([
    new ol.control.ScaleLine(),
    new ol.control.FullScreen(),
    new ol.control.OverviewMap(),
    /*new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(4),
    projection: 'EPSG:4326'
    })*/
  ]),
  view: new ol.View({
    center: ol.proj.fromLonLat([12, 50]),
    zoom: 5
  })
});

function mapCountryUpdate_remove(){
  for (var y=0; y<alpha3_countries.length; y++){
    map.removeLayer(window[alpha3_countries[y]]);
  }
}

var styleNotClicked = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: '#6ab6d4',
    width: 3
  })
});

var styleClicked = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: '#025dab',
    width: 3
  })
});

var styleWrong = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'rgba(224, 0, 0, 1)',
    width: 3
  })
});

var styleRight_answerGiven = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'rgba(0, 205, 0, 1)',
    width: 3
  })
});

var styleRight_answerNotGiven = new ol.style.Style({
  stroke: new ol.style.Stroke({
    color: 'rgba(255, 102, 0, 1)',
    width: 3
  })
});

function mapCountryUpdate_add(countries){
  alpha3_countries = countries
  extents = [];
  for (var p=0; p<alpha3_countries.length; p++){
    var vectorCountry = alpha3_countries[p];
    var sourceCountry = alpha3_countries[p] + "_source";
    window[sourceCountry] = new ol.source.Vector({
      url: window[alpha3_countries[p].toLowerCase() + "_source"],
      format: new ol.format.GeoJSON()
    });

    getExtent(sourceCountry);

    window[vectorCountry] = new ol.layer.Vector({
      source: window[sourceCountry],
      style: styleNotClicked
    });

    window[vectorCountry].setProperties({"title": vectorCountry});

    map.addLayer(window[vectorCountry]);
  }
}

function getExtent(sourceCountry){
  //console.log("getExtent()");
  window[sourceCountry].once('change',function(e){
    if(window[sourceCountry].getState() === 'ready') {
      var extent = window[sourceCountry].getExtent();
      //console.log(sourceCountry + " --- " + extent);
      extents.push(extent);
      //console.log(extents);
      if (extents.length == alpha3_countries.length)
      getFinalExtent();
    }
  });
}

function getFinalExtent(){
  var x1, y1, x2, y2, x1s=[], y1s=[], x2s=[], y2s=[];

  for (var m=0; m<extents.length; m++){
    x1s.push(extents[m][0]);
    y1s.push(extents[m][1]);
    x2s.push(extents[m][2]);
    y2s.push(extents[m][3]);
  }
  x1 = Math.min.apply(null, x1s);
  y1 = Math.min.apply(null, y1s);
  x2 = Math.max.apply(null, x2s);
  y2 = Math.max.apply(null, y2s);
  //console.log("FINAL--> " + "x1: " + x1  + " y1: " + y1 + " x2: " + x2 + " y2: " + y2);
  var finalExtent = ol.extent.boundingExtent([[x1, y1], [x2, y2]]);
  map.getView().fit(finalExtent, map.getSize());
}

function htmlGenerator(){
  var type = questionnaire.questions[i]._type;
  var right_answer = decrypt(questionnaire.questions[i].answer);
  //console.log(right_answer);
  var cnt_list = questionnaire.questions[i].cnt_list;
  //console.log("cnt_list: " + cnt_list);
  //cnt_list = ["ITA", "AFG"];
  var answers = [];
  //var right_answer = "sdtgadklrjtkalehrtg klòasdnflòand orhasdmfakòlmdjh oiq ertjhpqSF KLE RHIOEGUJOPDKJ fkldhfgoqihe nrgkjnadl kgho eirga lks dmgnlka hdf";
  var html = "";

  if (type == "MB"){
    answers = questionnaire.questions[i].answers;
    //console.log(answers);
    mapCountryUpdate_add(answers);
  }
  else {
    if (cnt_list.length == 1 && (cnt_list[0] == "Mediterranean" || cnt_list[0] == "Europe" || cnt_list[0] == "World")){
      //console.log("cnt_list[0]: " + cnt_list[0]);
      var finalExtent;
      switch (cnt_list[0]){
        case "Mediterranean":
          finalExtent = ol.extent.boundingExtent([[-1588153, 3158093], [4123370, 6225122]]);
          break;
        case "Europe":
          finalExtent = ol.extent.boundingExtent([[-3045174, 3995880], [4298212, 11426687]]);
          break;
        case "World":
          finalExtent = ol.extent.boundingExtent([[-19640644, -8767624], [19232678, 11397547]]);
          break;
      }
      map.getView().fit(finalExtent, map.getSize());
    }
    else
      mapCountryUpdate_add(cnt_list);
  }

  if (type == "TF"){
    var html = "<form id='tfForm'>" +
    "<label><input type='radio' name='tf' id='true'><span id='labelText'>TRUE</span></label><br>" +
    "<label><input type='radio' name='tf' id='false'><span id='labelText'>FALSE</span></label>" +
    "</form>";
  }
  else if (type == "TB"){
    html = "<span id='spanTextInput'><input id='textInput' placeholder='type here...' type='text'></span>";
    if (right_answer.indexOf("%") >= 0){
      html = "<span id='spanTextInput'><input id='textInput' placeholder='type here...' type='text'>%</span>";
    }
    //console.log(right_answer);
  }
  else if (type == "MB"){
    html = "<form id='mbForm'>" +
    "Select one of the countries " +
    "<i>" + questionnaire.questions[i].ans_cnt_names[0] + "</i>, " +
    "<i>" + questionnaire.questions[i].ans_cnt_names[1] + "</i>, " +
    "<i>" + questionnaire.questions[i].ans_cnt_names[2] + "</i>, " +
    "<i>" + questionnaire.questions[i].ans_cnt_names[3] + "</i>" +
    " <b>on the map</b>, then press the <i>Submit</i> button." +
    "<span id='thumb'></span>" +
    "</form>";
  }
  else {
    answers = questionnaire.questions[i].answers;
    html = "<form id='mcForm'>" +
    "<label><input type='radio' name='mc' id='one'><span id='labelText'>" + capitalizeFirstLetter(answers[0]) + "</span></label><br>" +
    "<label><input type='radio' name='mc' id='two'><span id='labelText'>" + capitalizeFirstLetter(answers[1]) + "</span></label><br>" +
    "<label><input type='radio' name='mc' id='three'><span id='labelText'>" + capitalizeFirstLetter(answers[2]) + "</span></label><br>" +
    "<label><input type='radio' name='mc' id='four'><span id='labelText'>" + capitalizeFirstLetter(answers[3]) + "</span></label>" +
    "</form>";
  }
  return html;
}

var submitButton = "<button id='submitButton' type='button'>Submit</button>";

function questionGenerator(){
  if (questionnaire.questions[i]._type == "MB"){
    if (ELdeactivated == true){
      mapClickKey = map.on('click', function(evt) {
        var feature = map.forEachFeatureAtPixel(evt.pixel,
          function(feature, layer) {
            title = layer.getProperties().title;
            return feature;
          }
        );
        if (feature){
          //console.log("title: " + title);
          if (window[title].getStyle() == styleNotClicked){
            window[title].setStyle(styleClicked);
            var index = alpha3_countries.indexOf(title);
            //console.log(index);
            for (var n=0; n<alpha3_countries.length; n++){
              if (n!=index)
              window[alpha3_countries[n]].setStyle(styleNotClicked);
            }
          }
          else if (window[title].getStyle() == styleClicked){
            window[title].setStyle(styleNotClicked);
          }

          alpha3_selected = feature.get("ISO3166_1_");
          //console.log(alpha3_selected);
        }
      });

      //change mouse cursor when over marker
      mapPointerMoveKey = map.on('pointermove', function(e) {
        var pixel = map.getEventPixel(e.originalEvent);

        var feature = map.forEachFeatureAtPixel(pixel,
          function(feature, layer) {
            return feature;
          }
        );

        var hit = (map.hasFeatureAtPixel(pixel));
        map.getTarget().style.cursor = hit ? 'pointer' : '';
      });
      ELdeactivated = false;
    }
  }
  else{
    map.unByKey(mapClickKey);
    map.unByKey(mapPointerMoveKey);
    map.getTarget().style.cursor = '';
    ELdeactivated = true;
  }

  return questionnaire.questions[i].question + "<br>" + htmlGenerator() + submitButton;
}

function startGame(){
  duration = 30;
  $('#timer').text(duration);
  i++;
  if(i < counter){
    submitButtonRemoved = false;
    question = questionGenerator();
    $("#questionnaire p").html(question);
    //console.log(i);
    //setTimeout(startGame, 10500);
    intervalID = setInterval(timerQuestion, 1000);
    function timerQuestion(){
      duration--;
      $('#timer').text(duration);
      if (duration < 1){
        window.clearInterval(intervalID);
        trem = 0;
        evaluateAnswer();
        //startGame();
      }
    }
    /*intervalID = setInterval(function () {
      duration--;
      $('#timer').text(duration);
      if (duration < 1){
        window.clearInterval(intervalID);
        trem = 0;
        evaluateAnswer();
        //startGame();
      }
    }, 1000);*/
  }
  else {
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    //sending the game results
    var gameResults_string = JSON.stringify(gameResults);
    //console.log(gameResults_string);
    $.ajax({
      type: "POST",
      url: "/migrate/finish/",
      data: gameResults_string,
      success: function(response){
        //console.log("score: " + response.score);
        var score = response.score;

        $("#questionnaire").css("visibility", "hidden");
        $('#questionnaire').removeClass("bigEntrance");
        $("#end #pFirst").html("Game is finished!<br>Your score is: " + score);
        if (score < 2){
          $('.box#end img').attr("src", badge_zero_one_source);
          $("#end #pSecond").html("Come on, you can do better than this!");
        }
        else if (score < 4){
          $('.box#end img').attr("src", badge_two_three_source);
          $("#end #pSecond").html("Not so bad, keep on playing!");
        }
        else if (score < 6){
          $('.box#end img').attr("src", badge_four_five_source);
          $("#end #pSecond").html("You’re almost there!");
        }
        else{
          $('.box#end img').attr("src", badge_six_source);
          $("#end #pSecond").html("Your knowledge is impressive, congratulations!");
        }
        $("#end").css("visibility", "visible");
        score = 0;
        questionnaire = {};
        gameResults = {};
      }
    });
  }
}

function evaluateAnswer() {
  var right_answer;
  var given_answer = "";
  var given_answerJSON = new Object();
  var type = questionnaire.questions[i]._type;
  var question_id = questionnaire.questions[i].id;
  given_answerJSON.question_id = question_id;

  var $thumb_up = ($("<img id='thumb_up' src='" + thumb_up_source + "'>"));
  var $thumb_down = ($("<img id='thumb_down' src='" + thumb_down_source + "'>"));

  if (type == "TF" || type == "MC") {
    right_answer = capitalizeFirstLetter(decrypt(questionnaire.questions[i].answer)); //needed only in the case of MC, but TF are already in all capital
    given_answer = $('input[type="radio"]:checked').parent().text();
    //console.log(given_answer + " --- " + right_answer);
    if (given_answer == right_answer) {
      //the answer is selected and it is right
      $('input[type="radio"]:checked').parent().css("color", "rgba(0, 205, 0, 1)");
      $('input[type="radio"]:checked').parent().css("font-weight", "bold");
      $('input[type="radio"]:checked').parent().append($thumb_up);
      $('input[type="radio"]:checked').parent().css("width", "calc(100% - 32px)");
      //the answer is selected and it is right
    }
    //nothing is selected, just show the right answer (given_answer == undefined)
    else if (given_answer == "") {
      $("span:contains('" + right_answer + "')").css("color", "rgba(255, 102, 0, 1)");
      $("span:contains('" + right_answer + "')").css("font-weight", "bold");
    }
    else {
      //the answer is selected and wrong, so highlight both wrong and right
      $("span:contains('" + right_answer + "')").css("color", "rgba(0, 205, 0, 1)");
      $("span:contains('" + right_answer + "')").css("font-weight", "bold");
      $('input[type="radio"]:checked').parent().css("color", "rgba(224, 0, 0, 1)");
      $('input[type="radio"]:checked').parent().css("font-weight", "bold");
      $('input[type="radio"]:checked').parent().append($thumb_down);
      $('input[type="radio"]:checked').parent().css("width", "calc(100% - 32px)");
    }
  }
  else if (type == "MB") {
    right_answer = decrypt(questionnaire.questions[i].answer_code);
    given_answer = alpha3_selected;
    //console.log("answers: " + questionnaire.questions[i].answers);
    //console.log("right answer: " + right_answer + " --- " + "alpha3_selected: " + alpha3_selected);
    if (right_answer == alpha3_selected) {
      //console.log("right!");
      $("#thumb").append($thumb_up);
      window[alpha3_selected].setStyle(styleRight_answerGiven);
      map.removeLayer(window[alpha3_selected]);
      map.addLayer(window[alpha3_selected]);
    }
    else if (alpha3_selected == "") {
      window[right_answer].setStyle(styleRight_answerNotGiven);
      map.removeLayer(window[right_answer]);
      map.addLayer(window[right_answer]);
    }
    else {
      $("#thumb").append($thumb_down);
      window[alpha3_selected].setStyle(styleWrong);
      map.removeLayer(window[alpha3_selected]);
      map.addLayer(window[alpha3_selected]);
      window[right_answer].setStyle(styleRight_answerGiven);
      map.removeLayer(window[right_answer]);
      map.addLayer(window[right_answer]);
    }
    map.unByKey(mapClickKey);
    map.unByKey(mapPointerMoveKey);
    map.getTarget().style.cursor = '';
    ELdeactivated = true;
  }
  else {
    right_answer = decrypt(questionnaire.questions[i].answer);
    given_answer = $("#textInput").val();
    var lowerBound, upperBound;

    var isNumber = false;
    if (isNaN(given_answer) == false)
      isNumber = true;

    if (right_answer.indexOf("%") >= 0){
      lowerBound = right_answer.slice(0, -1)*9/10;
      upperBound = right_answer.slice(0, -1)*11/10;
      //if (lowerBound < 0) lowerBound = 0;
      if (upperBound > 100) upperBound = 100;
    }
    else if (right_answer.indexOf("%") < 0){
      lowerBound = right_answer*8/10;
      upperBound = right_answer*12/10;
    }

    if (isNumber == false && given_answer != ""){
      alert("The answer is an integer!");
    }

    if(isNumber && given_answer >= lowerBound && given_answer <= upperBound){
      $("#textInput").css("color", "rgba(0, 205, 0, 1)");
      $("#textInput").css("font-weight", "bold");
      $('#spanTextInput').append($thumb_up);
    }
    else if (given_answer == ""){
      $("#textInput").css("color", "rgba(255, 102, 0, 1)");
      $("#textInput").css("font-weight", "bold");
      $("#textInput").val(right_answer);
    }
    else {
      $("#textInput").css("color", "rgba(224, 0, 0, 1)");
      $("#textInput").css("font-weight", "bold");
      $('#spanTextInput').append($thumb_down);
    }
  }
  given_answerJSON.answer = given_answer;
  given_answerJSON.trem = trem;
  gameResults.questions.push(given_answerJSON);

  if (submitButtonRemoved == false){
    $("#submitButton").remove();
    submitButtonRemoved = true;
    $("#questionnaire p").append("<button id='nextButton' type='button'>Next</button>");
    $("#questionnaire p").append("<b>Data source:</b> <a href= '" + questionnaire.questions[i].data_source_link + "' target='_blank'>" + questionnaire.questions[i].data_source + "</a><br>" + questionnaire.questions[i].help_text);
  }
}

$("#startButton").click(function() {
  $.getJSON("/migrate/game/restart/", function(data) {
    $("#noConnection").text("");    
    $("#start").css("visibility", "hidden");
    $("#questionnaire").css("visibility", "visible");
    $('#questionnaire').addClass("box bigEntrance");

    //console.log(data);
    questionnaire.questions = data.questions;
    //console.log(questionnaire);
    gameResults.game_id = questionnaire.questions[0].game_id;
    gameResults.questions = [];
    startGame();
  }).fail(function(){
    $("#noConnection").text("No internet connection!");
    //console.log("no internet connection");
  });
});

$("#closeButton").click(function() {  
  $("#end").css("visibility", "hidden");
  i=-1;
  $("#start").css("visibility", "visible");
});

$("#questionnaire").on('click', "#submitButton", function(){
  window.clearInterval(intervalID);
  trem = duration;
  evaluateAnswer();
});

$("#questionnaire").on('click', "#nextButton", function(){
  alpha3_selected = "";
  //window.clearInterval(intervalID);
  mapCountryUpdate_remove();
  startGame();
});
