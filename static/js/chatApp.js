var webSocket;

var webSocket= new WebSocket("ws://localhost:8888/ws");
webSocket.onmessage = function(e){
	response = JSON.parse(e.data);
	console.log(response);
	switch (response.header) {
		case "renderMain":
		renderMain(response);
		break;
		case "showMsg":
		showMsg(response);
		break;
		case"showGroupMsg":
		showGroupMsg(response);
		break;
	}
}

function start() {
	request =
	{
		'header':'start',
		'userName':$('#userName').val()
	}
	webSocket.send(JSON.stringify(request));
}
function slider() {
  $("#flexiselDemo1").flexisel();
  $("#flexiselDemo2").flexisel();
}
function renderMain(response) {
	$("#name").html("<small>Welcome </small>"+response.user.name);
  $("#online_people, #online_group, #flexiselDemo1, #flexiselDemo2").html("");
	$(response.user.friends).each(function(i,elmt) {
		$("#online_people").append(
      `<table>
        <tr class="ppl">
          <td>
          <a id="`+elmt.name+`" href="#" `+(elmt.status ? 'onclick="startChat(event,\''+elmt.name+'\')"':'' )+`>  <img id="`+elmt.name+`_img" src="../static/img/`+ (Math.floor(Math.random()*7)+1) +`.png" /> </a>
          </td>
          <td>
            `+elmt.name+`
          </td>
          <td>
            <img class="status" src="../static/img/`+ (elmt.status ? 'green' : 'gray' )+`.png" />
          </td>
          <td id="deleteBtn" >
          <a href="#" onclick="removeFriend(event,'`+elmt.name+`')">
          <span class="glyphicon glyphicon-remove"></span>
          </a>
          </td>
        </tr>
      </table>`);
	})
	$(response.user.groups).each(function(i,elmt) {
		$("#online_group").append(
      `	<table>
					<tr>
						<td>
						<a id="`+elmt.group_name+`" href="#" onclick="startChat(event,'`+elmt.group_name+`') ">
							<img id="`+elmt.group_name+`_img" src="../static/img/g`+(Math.floor(Math.random()*2)+1)+`.png" />
						</a>
						</td>
						<td>
								`+elmt.group_name+`
						</td>
            <td id="deleteBtn" >
            <a href="#" onclick="leaveGroup(event,'`+elmt.group_name+`')">
            <span class="glyphicon glyphicon-remove"></span>
            </a>
            </td>
					</tr>
				</table>`);
	})
	$(response.user.availFriends).each(function(i,elmt) {
		$("#flexiselDemo1").append(
      `<li  onclick="addFriend('`+elmt.name+`')"><img src="../static/img/`+ (Math.floor(Math.random()*7)+1) +`.png" />`+elmt.name+` </li>`);
	})
	$(response.user.availGroups).each(function(i,elmt) {
		$("#flexiselDemo2").append(
      `<li><a  onclick="joinGroup(event,'`+elmt.group_name+`')"><img src="../static/img/g`+(Math.floor(Math.random()*2)+1)+`.png" />`+elmt.group_name+`</a></li>`
			);
	})
	$("#welcome").hide();
	$("#container").show();
	slider();
}
function addFriend(friendName) {
  request =
	{
		'header':'addFriend',
		'input': friendName
	}
	webSocket.send(JSON.stringify(request));
}
function removeFriend(e,friendName) {
  e.preventDefault();
  request =
	{
		'header':'removeFriend',
		'input': friendName
	}
	webSocket.send(JSON.stringify(request));
}
function joinGroup(e,group_name) {
  e.preventDefault();
  request =
	{
		'header':'joinGroup',
		'input': group_name
	}
	webSocket.send(JSON.stringify(request));
}
function leaveGroup(e,group_name){
  e.preventDefault();
  request =
	{
		'header':'leaveGroup',
		'input': group_name
	}
	webSocket.send(JSON.stringify(request));
}
function createGroup() {
	request =
	{
		'header':'createGroup',
		'input':$('#groupName').val()
	}
	webSocket.send(JSON.stringify(request));
	$('#groupName').val("");
}
function startChat(e,chatter) {
	e.preventDefault();
	$("#groupAdd, #all_people, #all_groups").hide();
	$("#chat").children().hide();
	if ($("#"+chatter+"_div").length) {
		$("#"+chatter+"_div").show();
	}else{
		$("#chat").append(`
			<div id='`+chatter+`_div' style="width:670px;height:430px;margin:20px;padding:5px;overflow-y:auto;">
				<img src="`+$("#"+chatter+"_img")[0].src+`" style="float:left;"/>
				<h3 class="text-left text-primary" style="float:left;">`+chatter+`</h3><a href="#" onclick="closeChat(event,'`+chatter+`')">
				<span class="glyphicon glyphicon-remove "></span>
				</a>
				<div id="`+chatter+`_chatDisplay" class="chatDisplay"></div>
				<form action="" class="form-inline" >
				<input type="text" id="`+chatter+`_msg" class="form-control text-left" style="width:85%;" placeholder="Enter your Text Here ... ">
				<button type="button" class="form-control btn-success btn-xs" onclick="sendMsg('`+chatter+`')">Send</button>
				</form>
			</div>
			`).show();
	}
}
function closeChat(e,chatter) {
	e.preventDefault();
	$("#"+chatter+"_div").hide();
	$("#groupAdd, #all_people, #all_groups").show();
}
function sendMsg(chatter) {
	$("#"+chatter+"_chatDisplay").append(`<h4> Me: <small>`+$("#"+chatter+"_msg").val()+`</small></h4>`);
	request =
	{
		'header':'sendMsg',
		'to':chatter,
		'msg':$("#"+chatter+"_msg").val()
	}
	webSocket.send(JSON.stringify(request));
	$("#"+chatter+"_msg").val("");

}
function showMsg(response) {
	$("#groupAdd, #all_people, #all_groups").hide();
	$("#chat").children().hide();
	if ($("#"+response.from+"_div").length) {

		$("#"+response.from+"_div").show();
	}else{
		$("#"+response.from+"").click();
	}
	$("#"+response.from+"_chatDisplay").append(`<h4> `+response.from+`: <small>`+response.msg+`</small></h4>`);
}
function showGroupMsg(response) {
	$("#groupAdd, #all_people, #all_groups").hide();
	$("#chat").children().hide();
	if ($("#"+response.group+"_div").length) {

		$("#"+response.group+"_div").show();
	}else{
		$("#"+response.group+"").click();
	}
	$("#"+response.group+"_chatDisplay").append(`<h4> `+response.from+`: <small>`+response.msg+`</small></h4>`);
}
