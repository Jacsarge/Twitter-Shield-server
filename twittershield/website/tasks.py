from __future__ import absolute_import
from celery import shared_task, current_task
from celery.exceptions import Ignore
from website.models import TwitterAccount, Tweet
from django.contrib.auth.models import User
from website.views import get_user_timeline, clean_tweets, get_tweet_perspective_scores, get_user_perspective_score, store_tweets
from django.utils import timezone
import tweepy


PERSPECTIVE_MODELS = ['TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY','THREAT','SEXUALLY_EXPLICIT', 'FLIRTATION']
TWEET_BATCH_NUM = 3
APPROX_BATCH_SIZE = 200/TWEET_BATCH_NUM
TWEET_COUNT = 200

@shared_task
def get_score(screen_name, threshold):
	user_perspective_scores = {}
	try:
		twitter_account = TwitterAccount.objects.filter(screen_name=screen_name)
		if twitter_account.count() == 0:
			# print("NEW STORE")
		
			#models user choses  + score - probably store this in db too! 
			#set default as zero in front end 
			twitter_account = TwitterAccount.objects.create(screen_name=screen_name,
															stored_at = timezone.now(),
															recent_tweet_count=0)


			#get tweets on user's timeline
			# print('get tweets')
			user_timeline_tweets = get_user_timeline(screen_name, TWEET_COUNT)
			# not authorized or no tweets at all
			if user_timeline_tweets == 'Not authorized.' or len(user_timeline_tweets) == 0:
				twitter_account.toxicity_score = -1
				twitter_account.save()
			else:
				# print('here ' + str(len(user_timeline_tweets)))
				cleaned_user_timeline_tweets = clean_tweets(user_timeline_tweets)	
				
				#  if no English tweets
				if len(cleaned_user_timeline_tweets) == 0:
					twitter_account.toxicity_score = -1
					twitter_account.save()
				else:
					models_setting_json = {}
					for model in PERSPECTIVE_MODELS:
						# print(model)
						models_setting_json[model] = {'scoreThreshold': '0'}
						# if(request.GET.get(model.lower())):
						# 	models_setting_json[model] = {'scoreThreshold': request.args.get(model.lower())}
						# else:
						# 	models_setting_json[model] = {'scoreThreshold': '0'}
					
					tweets_with_perspective_scores = get_tweet_perspective_scores(cleaned_user_timeline_tweets, models_setting_json, twitter_account)
					user_perspective_scores = get_user_perspective_score(tweets_with_perspective_scores)
					# failed
					if user_perspective_scores is None:
						twitter_account.delete()
						print('FAILED')
					else:
						# insert into db
						user_perspective_scores['username'] = screen_name
						user_perspective_scores['tweets_considered_count'] = len(tweets_with_perspective_scores)
						user_perspective_scores['tweets_with_scores'] = tweets_with_perspective_scores
						score = str(user_perspective_scores['TOXICITY']['score'])
						# print('threshold' + threshold)
						print('score: ' + score)

						# if (float(score) >= float(threshold)):
						# 	print("ABOVE")
						# 	user_perspective_scores['visualize'] = score
						# else:
						# 	print("BELOW")
						# 	user_perspective_scores['visualize'] = 'Below threshold'
				

						twitter_account.toxicity_score=score
						twitter_account.identity_attack_score = user_perspective_scores['IDENTITY_ATTACK']['score']
						twitter_account.insult_score = user_perspective_scores['INSULT']['score']
						twitter_account.profanity_score = user_perspective_scores['PROFANITY']['score']
						twitter_account.threat_score = user_perspective_scores['THREAT']['score']
						twitter_account.sexually_explicit_score = user_perspective_scores['SEXUALLY_EXPLICIT']['score']
						twitter_account.flirtation_score = user_perspective_scores['FLIRTATION']['score']
						twitter_account.stored_at = timezone.now()
						twitter_account.recent_tweet_count=len(tweets_with_perspective_scores)
						twitter_account.save()		
						# print("IDENTITY_ATTACK: " + str(twitter_account.identity_attack_score))
						# print("INSULT: "+ str(twitter_account.insult_score))
						# print("PROFANITY: "+ str(twitter_account.profanity_score))	

		else:
			print("ALREADY STORED!")


	except Exception as e:
		print(e)

	# return user_perspective_scores
	# return JsonResponse(user_perspective_scores)

