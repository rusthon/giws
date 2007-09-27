#!/usr/bin/python -u
from types import MethodType

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	JNIEnvVariable="JEnv"
	JNIEnvVariableType="JNIEnv"
	JavaVMVariable="jvm"
	JavaVMVariableType="JavaVM"
	
	def getHeader(self):
		return """#include <string>
		#include <iostream>
		#include <stdlib.h>
		#include <jni.h>
		"""

	def JNIEnvAccess(self):
		return ("""%s->""" % self.JNIEnvVariable)

	def getJNIEnvVariable(self):
		return self.JNIEnvVariable
	
	def getJNIEnvVariableType(self):
		return self.JNIEnvVariableType
	
	def getJavaVMVariable(self):
		return self.JavaVMVariable
	
	def getJavaVMVariableType(self):
		return self.JavaVMVariableType

	def getMethodGetCurrentEnv(self,objectName):
		return """
		JNIEnv * %s::getCurrentEnv() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread((void **) &curEnv, NULL);
		return curEnv;
		}"""%(objectName)

	
	def getObjectInstanceProfile(self):		
		return """
		JNIEnv * curEnv = getCurrentEnv();


		""" 

	def getMethodIdProfile(self,method):
		params=""
		for parameter in method.getParameters():
			params+=parameter.getType().getTypeSignature()

		methodIdName=method.getUniqueNameOfTheMethod()
		return ("""
		if (this->%s == NULL)
		{
		this->%s = curEnv->GetMethodID(this->instanceClass, "%s", "(%s)%s" ) ;
		if (this->%s == NULL) {
		std::cerr << "Could not access to the method %s" << std::endl;
		exit(EXIT_FAILURE);
		}
		}""")%(methodIdName, methodIdName, method.getName(), params, method.getReturn().getTypeSignature() ,methodIdName, method.getName())

	def getCallObjectMethodProfile(self,method):
		parametersTypes=method.getParameters()
		returnType=method.getReturn()
		i=1
		params=""
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
		else:
			returns="""%s res ="""%returnType.getJavaTypeSyntax()

		return ("""
	 	%s (%s) curEnv->%s( this->instance, %s %s);
""" % (returns, returnType.getJavaTypeSyntax(),   returnType.CallMethod(), method.getUniqueNameOfTheMethod(), params ))

	def getReturnProfile(self, returnType):
		
		if hasattr(returnType, "specificReturn") and type(returnType.specificReturn) is MethodType: # When a specific kind of return is necessary (string for example)
			return returnType.specificReturn()
		else:
			return """
			return res;
			"""
		
