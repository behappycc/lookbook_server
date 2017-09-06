import numpy as np



def rank(result_predict):
	result_order = np.argsort(result_predict)

	top5= result_order[0][-5:] 
	top5=top5[::-1]


	result_rank=np.empty([6, 2])

	
	for i in range(5):
		result_rank[i][0]=top5[i]
		# print top5[i]      # city index
		result_rank[i][1]=result_predict[0][top5[i]]
		# print result_predict[0][top5[i]]     # city_posibility
		# result_rank[i][1] = round(result_rank[i][1], 3)
		result_rank[i][1] = round(result_rank[i][1]/0.01, 1)     # float to percentage

		# print result_rank[i][1]

	city_rank=result_rank.tolist()

	readCities = open('./cities.txt', 'r')
	citiesList = readCities.read().split('\n')

	for i in range(5):
		city_rank[i][0]=citiesList[int(city_rank[i][0])]
		# print city_rank[i][0]  # city name
	# print result_order

	other = 0
	for i in range(5):
		other += result_rank[i][1]
	other = round(100-other, 1)

	city_rank[5][0] = 'others:'
	city_rank[5][1] = other

	return city_rank

