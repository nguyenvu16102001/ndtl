# -*- coding: utf-8 -*- 


class SITRequest(object):

	def get_params(payload=None, required_params:list=None, optional_params:list=None):
		if not payload:
			payload = dict()
		results = [None] * (len(required_params or list()) + len(optional_params or list()))
		for i in range(len(required_params)):
			results[i] = payload.get(required_params[i])
		required_params_len = len(required_params)
		for j in range(len(optional_params)):
			results[required_params_len+j] = payload.get(optional_params[j])
		return results
