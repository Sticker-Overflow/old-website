import os, sys, json, logging, requests, uuid, random, string, subprocess

import cyclone.web, cyclone.httpclient, cyclone.websocket
from cyclone.bottle import run

from twisted.internet import reactor, ssl
from twisted.python import log

from PIL import Image

from OpenSSL import crypto

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google.cloud.exceptions

# Use a service account
cred = credentials.Certificate(getFirebaseCredentialsPath())
firebase_admin.initialize_app(cred)

db = firestore.client()

version = "0.0.1"

google_auth_client_secret = getGoogleAuthClientSecret()

class Hackathon(object):
	def __init__(self, id, name, location, dateString, date, logoURL, splashURL, url):
		self.id = id
		self.name = name
		self.location = location
		self.dateString = dateString
		self.date = date
		self.logoURL = logoURL
		self.splashURL = splashURL
		self.url = url

	@staticmethod
	def from_dict(source):
		hackathon = Hackathon(source["id"], source["name"], source["location"], source["dateString"], source["date"], source["logoURL"], source["splashURL"], source["url"])
		return hackathon

	def to_dict(self):
		dest = {
			'id': self.id,
			'name': self.name,
			'location': self.location,
			'dateString': self.dateString,
			'date': self.date,
			'logoURL': self.logoURL,
			'splashURL': self.splashURL,
			'url': self.url
		}

		return dest

	def __repr__(self):
		return u'Hackathon(id={}, name={}, location={}, dateString={}, date={}, logoURL={}, splashURL={}, url={})'.format(
			self.id, self.name, self.location, self.dateString, self.date, self.logoURL, self.splashURL, self.url)

class Sticker(object):
	def __init__(self, id, name, description, dateAdded, numberOfUsersWhoHaveThisSticker, purchaseUrl):
		self.id = id
		self.name = name
		self.description = description
		self.dateAdded = dateAdded
		self.numberOfUsersWhoHaveThisSticker = numberOfUsersWhoHaveThisSticker
		self.purchaseUrl = purchaseUrl

	@staticmethod
	def from_dict(source):
		sticker = Sticker(source["id"], source["name"], source["description"], source["dateAdded"], source["numberOfUsersWhoHaveThisSticker"], source["purchaseUrl"])
		return sticker

	def to_dict(self):
		dest = {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'dateAdded': self.dateAdded,
			'numberOfUsersWhoHaveThisSticker': self.numberOfUsersWhoHaveThisSticker,
			'purchaseUrl': self.purchaseUrl
		}
		return dest

	def __repr__(self):
		return u'Sticker(id={}, name={}, description={}, dateAdded={}, numberOfUsersWhoHaveThisSticker={}, purchaseUrl={})'.format(
			self.id, self.name, self.description, self.dateAdded, self.numberOfUsersWhoHaveThisSticker, self.purchaseUrl)

class Conversation(object):
	def __init__(self, id, lastModified, latestMessage, numberOfUnreadMessages, otherUserId):
		self.id = id
		self.lastModified = lastModified
		self.latestMessage = latestMessage
		self.numberOfUnreadMessages = numberOfUnreadMessages
		self.otherUserId = otherUserId

	@staticmethod
	def from_dict(source):
		conversation = Conversation(source["id"], source["lastModified"], source["latestMessage"], source["numberOfUnreadMessages"], source["otherUserId"])
		return conversation

	def to_dict(self):
		dest = {
			'id': self.id,
			'lastModified': self.lastModified,
			'latestMessage': self.latestMessage,
			'numberOfUnreadMessages': self.numberOfUnreadMessages,
			'otherUserId': self.otherUserId,
		}
		return dest

	def __repr__(self):
		return u'Conversation(id={}, lastModified={}, latestMessage={}, numberOfUnreadMessages={}, otherUserId={})'.format(
			self.id, self.lastModified, self.latestMessage, self.numberOfUnreadMessages, self.otherUserId)

class User(object):
	def __init__(self, uid, name, photoUrl, memberOrganizationId):
		self.uid = uid
		self.name = name
		self.photoUrl = photoUrl
		self.memberOrganizationId = memberOrganizationId

	@staticmethod
	def from_dict(source):
		user = User(source["uid"], source["name"], source["photoUrl"], source["memberOrganizationId"])
		return user

	def to_dict(self):
		dest = {
			'uid': self.uid,
			'name': self.name,
			'photoUrl': self.photoUrl,
			'memberOrganizationId': self.memberOrganizationId,
		}
		return dest

	def __repr__(self):
		return u'User(uid={}, name={}, photoUrl={}, memberOrganizationId={})'.format(
			self.uid, self.name, self.photoUrl, self.memberOrganizationId)

class Sponsor(object):
	def __init__(self, id, name, location, description, logoUrl, url):
		self.id = id
		self.name = name
		self.location = location
		self.description = description
		self.logoURL = logoURL
		self.url = url

	@staticmethod
	def from_dict(source):
		sponsor = Sponsor(source["id"], source["name"], source["location"], source["description"], source["logoURL"], source["url"])
		return sponsor

	def to_dict(self):
		dest = {
			'id': self.id,
			'name': self.name,
			'location': self.location,
			'description': self.description,
			'logoURL': self.logoURL,
			'url': self.url
		}
		return dest

	def __repr__(self):
		return u'Sponsor(id={}, name={}, location={}, description={}, logoURL={}, url={})'.format(
			self.id, self.name, self.location, self.description, self.logoURL, self.url)

class Organizer(object):
	def __init__(self, id, name, location, description, logoUrl, url):
		self.id = id
		self.name = name
		self.location = location
		self.description = description
		self.logoURL = logoURL
		self.url = url

	@staticmethod
	def from_dict(source):
		organizer = Organizer(source["id"], source["name"], source["location"], source["description"], source["logoURL"], source["url"])
		return organizer

	def to_dict(self):
		dest = {
			'id': self.id,
			'name': self.name,
			'location': self.location,
			'description': self.description,
			'logoURL': self.logoURL,
			'url': self.url
		}
		return dest

	def __repr__(self):
		return u'Organizer(id={}, name={}, location={}, description={}, logoURL={}, url={})'.format(
			self.id, self.name, self.location, self.description, self.logoURL, self.url)

ssl_certificate_path = "/etc/letsencrypt/live/stickeroverflow.io/cert.pem"
ssl_certificate_key_path = "/etc/letsencrypt/live/stickeroverflow.io/privkey.pem"
ssl_certificate_chain_path = "/etc/letsencrypt/live/stickeroverflow.io/chain.pem"
ssl_certificate_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(ssl_certificate_key_path, 'rt').read())
ssl_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, open(ssl_certificate_path, 'rt').read())
ssl_certificate_chain = [crypto.load_certificate(crypto.FILETYPE_PEM, open(ssl_certificate_chain_path, 'rt').read())]

root = os.path.join(os.path.dirname(__file__), ".")

subdomains = ["conversations", "users", "stickers", "hackathons", "sponsors", "organizers", "account", "identify"]

class BaseHandler(cyclone.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("cUid")

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")

	def prepare(self):
		if not self.current_user:
			if self.request.host != "stickeroverflow.io" or self.request.uri != "/":
				self.redirect("http://stickeroverflow.io")
		elif self.request.host == "stickeroverflow.io" and self.request.uri == "/":
			self.redirect("http://stickers.stickeroverflow.io")
		
		if self.request.host.split(".")[0] == "www":
			self.redirect("http://" + self.request.host.replace("www.", ""), permanent=False)

		if self.request.host == "stickeroverflow.io":
			if self.request.uri != "/":
				if len(self.request.uri.split("/")) == 2:
					self.redirect("http://" + self.request.uri.split("/")[1] + "." + self.request.host)
				elif len(self.request.uri.split("/")) == 3:
					self.redirect("http://" + self.request.uri.split("/")[1] + "." + self.request.host + "/" + self.request.uri.split("/")[2])
		elif self.request.host.split(".")[0] in subdomains:
			if self.request.uri != "/":
				if len(self.request.uri.split("/")) == 2:
					if self.request.uri.split("/")[1] in subdomains:
						self.redirect("http://" + self.request.uri.split("/")[1] + ".stickeroverflow.io" )
				elif len(self.request.uri.split("/")) == 3:
					if self.request.uri.split("/")[1] in subdomains:
						self.redirect("http://" + self.request.uri.split("/")[1] + ".stickeroverflow.io/" + self.request.uri.split("/")[2])
		
		if self.request.protocol == "http":
			self.redirect("https://%s" % self.request.full_url()[len("http://"):], permanent=True)

class ErrorHandler(BaseHandler):
	def __init__(self, application, request, status_code):
		cyclone.web.RequestHandler.__init__(self, application, request)
		self.set_status(status_code)

	def get_error_html(self, status_code, **kwargs):
		# If the status of the request is in the list, render that page
		if not self.current_user:
			self.redirect("http://stickeroverflow.io")
		else:
			if status_code in [404, 500, 503, 403]:
				self.render(str(status_code) + ".html")
	def prepare(self):
		raise cyclone.web.HTTPError(self._status_code)

cyclone.web.ErrorHandler = ErrorHandler

class MyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, datetime.datetime):
			encoded_object = list(obj.timetuple())[0:6]
		else:
			encoded_object =json.JSONEncoder.default(self, obj)
		return encoded_object

class MainHandler(BaseHandler):
	def get(self):
		self.render("index.html")

class IdentifyStickerHandler(BaseHandler):
	def get(self):
		self.render("identify.html")

class AccountHandler(BaseHandler):
	def get(self):
		tryToRenderPage(self, "users", self.current_user, "account.html")	

class HackathonsHandler(BaseHandler):
	def get(self):
		self.render("hackathons.html")

class SpecificHackathonHandler(BaseHandler):
	def get(self, hackathonId):
		tryToRenderPage(self, "hackathons", hackathonId, "hackathon.html")

class SponsorsHandler(BaseHandler):
	def get(self):
		self.render("sponsors.html")

class SpecificSponsorHandler(BaseHandler):
	def get(self, sponsorId):
		tryToRenderPage(self, "sponsors", sponsorId, "sponsor.html")

class OrganizersHandler(BaseHandler):
	def get(self):
		self.render("organizers.html")

class SpecificOrganizerHandler(BaseHandler):
	def get(self, organizerId):
		tryToRenderPage(self, "organizers", organizerId, "organizer.html")

class StickersHandler(BaseHandler):
	def get(self):
		self.render("stickers.html")

class SpecificStickerHandler(BaseHandler):
	def get(self, stickerId):
		tryToRenderPage(self, "stickers", stickerId, "sticker.html")

class UsersHandler(BaseHandler):
	def get(self):
		self.render("users.html")

class SpecificUserHandler(BaseHandler):
	def get(self, userId):
		tryToRenderPage(self, "users", userId, "user.html")

class ConversationsHandler(BaseHandler):
	def get(self):
		self.render("conversations.html")

class SpecificConversationHandler(BaseHandler):
	def get(self, conversationId):
		tryToRenderConversationPage(self, self.get_secure_cookie("cUid"), conversationId)

class WebStickerUploadedHandler(cyclone.web.RequestHandler):
	def post(self):
		photo = self.request.files['picture'][0]
		original_fname = photo['filename']
		extension = os.path.splitext(original_fname)[1]
		filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
		final_filename= filename+extension
		output_file = open("../images/uploads/" + final_filename, 'wb')
		output_file.write(photo['body'])
		output_file.close()

		process = subprocess.Popen("python3.5 -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=../images/uploads/" + final_filename, shell=True, stdout=subprocess.PIPE, cwd="../tensorflow/")

		out, err = process.communicate()

		splitOut = out.decode("utf-8").split("s\n")[1:]
		splitOutJoined = "".join(splitOut)
		splitOutJoinedReplaced = splitOutJoined.replace("\n", ",").replace(" 0.", ":0.").replace(" ", "-")
		splitOutJoinedReplacedSplit = splitOutJoinedReplaced.split(",")[1:-1]
		finalResult = ",".join(splitOutJoinedReplacedSplit)

		self.write({"Result": finalResult})
		self.finish()

class AndroidStickerUploadHandler(cyclone.web.RequestHandler):
	def post(self):
		file1 = self.request.files['picture'][0]
		original_fname = file1['filename']
		extension = os.path.splitext(original_fname)[1]
		fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
		final_filename= fname+extension
		output_file = open("../images/uploads/" + final_filename, 'wb')
		output_file.write(file1['body'])
		output_file.close()

		img = Image.open("../images/uploads/" + final_filename)
		rimg = img.transpose(Image.ROTATE_270)
		rimg.save("../images/uploads/" + final_filename)

		process = subprocess.Popen("python3.5 -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=../images/uploads/" + final_filename, shell=True, stdout=subprocess.PIPE, cwd="../tensorflow/")

		out, err = process.communicate()

		sp = out.decode("utf-8").split("s\n")[1:]
		j = "".join(sp)
		r = j.replace("\n", ",").replace(" 0.", ":0.").replace(" ", "-")
		m = r.split(",")[1:-1]
		mj = ",".join(m)

		self.write({"result": mj})
		self.finish()

class SignInHandler(cyclone.web.RequestHandler):
	def post(self):
		args = convertRequestArgs(self.request.body)
		try:
			userDoc = db.collection("users").document(args["uid"]).get()
			self.write(json.dumps({"Result": True}));
			self.set_secure_cookie("cUid", args["uid"], domain="stickeroverflow.io")
		except google.cloud.exceptions.NotFound:
			self.write(json.dumps({"Result": False}, separators=(', ', ': '), cls=MyEncoder));

class SignOutHandler(cyclone.web.RequestHandler):
	def get(self):
		self.redirect("http://stickeroverflow.io")

def tryToRenderPage(self, collectionName, documentId, page):
	try:
		doc = db.collection(collectionName).document(documentId).get()
		self.render(page, documentData=doc.to_dict())
	except google.cloud.exceptions.NotFound:
		self.render("404.html")

def tryToRenderConversationPage(self, userId, conversationId):
	try:
		doc = db.collection("users").document(userId).collection("conversations").document(conversationId).get()
		self.render("conversation.html", conversation=doc.to_dict())
	except google.cloud.exceptions.NotFound:
		self.render("404.html")

def convertRequestArgs(args):
	return json.loads(args)

if __name__ == "__main__":
	log.startLogging(sys.stdout)

	application = cyclone.web.Application([
		(r"/", MainHandler),

		(r"/identify", IdentifyStickerHandler),

		(r"/account", AccountHandler),

		(r"/web_upload", WebStickerUploadedHandler),
		(r"/android_upload", AndroidStickerUploadHandler),

		(r"/signin", SignInHandler),
		(r"/signout", SignOutHandler),

		(r"/hackathons", HackathonsHandler),
		(r"/hackathons/([a-zA-Z_\-0-9]+)", SpecificHackathonHandler),

		(r"/stickers", StickersHandler),
		(r"/stickers/([a-zA-Z_\-0-9]+)", SpecificStickerHandler),

		(r"/users", UsersHandler),
		(r"/users/([a-zA-Z_\-0-9]+)", SpecificUserHandler),

		(r"/sponsors", SponsorsHandler),
		(r"/sponsors/([a-zA-Z_\-0-9]+)", SpecificSponsorHandler),

		(r"/organizers", OrganizersHandler),
		(r"/organizers/([a-zA-Z_\-0-9]+)", SpecificOrganizerHandler),

		(r"/conversations", ConversationsHandler),
		(r"/conversations/([a-zA-Z_\-0-9]+)", SpecificConversationHandler),

		(r"/static/(.*)", cyclone.web.StaticFileHandler, {'path': os.path.join(root, 'static')})
	], cookie_secret=getCookieSecret(), template_path="./views", debug=True)

	# Allows for wildcard subdomain (assuming dns is configured)
	application.add_handlers(r"^hackathons.stickeroverflow.io$",
		[
			(r"/", HackathonsHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificHackathonHandler)
		]
	)

	application.add_handlers(r"^sponsors.stickeroverflow.io$",
		[
			(r"/", SponsorsHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificSponsorHandler)
		]
	)

	application.add_handlers(r"^organizers.stickeroverflow.io$",
		[
			(r"/", OrganizersHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificOrganizerHandler)
		]
	)

	application.add_handlers(r"^users.stickeroverflow.io$",
		[
			(r"/", UsersHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificUserHandler)
		]
	)

	application.add_handlers(r"conversations.stickeroverflow.io",
		[
			(r"/", ConversationsHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificConversationHandler)
		]
	)

	application.add_handlers(r"^stickers.stickeroverflow.io$",
		[
			(r"/", StickersHandler),
			(r"/signout", SignOutHandler),
			(r"/([a-zA-Z_\-0-9]+)", SpecificStickerHandler)
		]
	)

	application.add_handlers(r"^account.stickeroverflow.io$",
		[
			(r"/", AccountHandler),
		]
	)

	application.add_handlers(r"^identify.stickeroverflow.io$",
		[
			(r"/", IdentifyStickerHandler),
			(r"/signout", SignOutHandler),
		]
	)

	reactor.listenTCP(80, application)

	reactor.listenSSL(443, application,
	 	ssl.CertificateOptions(	privateKey=ssl_certificate_key,
	 				certificate=ssl_certificate,
	 				extraCertChain=ssl_certificate_chain))

	reactor.run()
