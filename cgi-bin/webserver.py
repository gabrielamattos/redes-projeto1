#!/usr/bin/python
# -*- coding: utf-8 -*- 

#################################################################################################################
# 	Nome: webserver.py											#
# 	Autor: Gabriela Mattos											#
# 	Objetivo: interface web que recebe as instruções do browser do usuário.					#
# 	Referências:												#
# - http://www.tutorialspoint.com/python/python_cgi_programming.htm 						#
#################################################################################################################
import cgi, cgitb
import backend

form = cgi.FieldStorage()

print "Content-type:text/html"
print
response = ""

for i in range(3):

	if form.getvalue('selPsM'+str(i+1)):
		mensagem = "REQUEST " + " 1 " + form.getvalue('ArgPsM'+str(i+1))
		response.append(backend.sendMsg(mensagem))
	if form.getvalue('selDfM'+str(i+1)):
		mensagem = "REQUEST " + " 2 " + form.getvalue('ArgDfM'+str(i+1))
		response.append(backend.sendMsg(mensagem))
	if form.getvalue('selFingerM'+str(i+1)):
		mensagem = "REQUEST " + " 3 " + form.getvalue('ArgFingerM'+str(i+1))
		response.append(backend.sendMsg(mensagem))
	if form.getvalue('selUpTimeM'+str(i+1)):
		mensagem = "REQUEST " + " 4 " + form.getvalue('ArgUpTimeM'+str(i+1))
		response.append(backend.sendMsg(mensagem))

print "%s" % response
