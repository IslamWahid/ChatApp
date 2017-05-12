from tornado import web,websocket
from models.user import User
from models.group import Group

import json

sockets = []
class WSHandler(websocket.WebSocketHandler):

	def on_close(self):
		sockets.remove(self)
		self.renderAllPeopleMain()

	def on_message(self,message):
		request = json.loads(message)
		if request['header'] == 'start' and request['userName'] != None:
			self.userObj=User(request['userName'])
			sockets.append(self)
			for c in sockets:
				c.renderMain()

		elif request['header'] == 'addFriend':
			self.userObj.addFriend(request['input'])
			self.renderMain()
		elif request['header'] == 'removeFriend':
			self.userObj.removeFriend(request['input'])
			self.renderMain()
		elif request['header'] == 'joinGroup':
			self.userObj.joinGroup(request['input'])
			self.renderMain()
		elif request['header'] == 'leaveGroup':
			self.userObj.leaveGroup(request['input'])
			self.renderMain()
		elif request['header'] == 'createGroup':
			self.userObj.createGroup(request['input'])
			self.renderAllPeopleMain()
		elif request['header'] == 'sendMsg':
			self.sendMsg(request)

	def renderMain(self):
		user = self.userObj
		user.setAllUserData()
		onlineUsersIds=[o.userObj.id for o in sockets]
		for friend in user.friends:
			if friend['id'] in onlineUsersIds:
				friend['status']= True
			else:
				friend['status'] = False
		response = {'header':'renderMain' ,
		'user':user.__dict__
		}
		self.write_message(json.dumps(response))

	def renderAllPeopleMain(self):
		for c in sockets:
			c.renderMain()

	def sendMsg(self, request):
		if request['to'] in [o.userObj.name for o in sockets]:
			for c in sockets :
				if c.userObj.name == request['to'] :
					response = {'header':'showMsg' ,
					'from':self.userObj.name,
					'msg':request['msg']
					}
					c.write_message(json.dumps(response))
		else:
			group=Group(request['to'])
			members=group.getAllGroupMembers()
			groupMembersIds=[o['user_id'] for o in members]
			for c in sockets :
				if c.userObj.id in groupMembersIds and c.userObj.id != self.userObj.id:
					response = {'header':'showGroupMsg' ,
					'from':self.userObj.name,
					'group':request['to'],
					'msg':request['msg']
					}
					c.write_message(json.dumps(response))
