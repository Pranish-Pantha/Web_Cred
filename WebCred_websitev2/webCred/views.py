from django.http import HttpResponse
from django.shortcuts import render
from .forms import urlForm, jobForm, articleNameForm
from .networkPreds import predictorNLP
import requests
from bs4 import BeautifulSoup


predictor = predictorNLP()
jobSearches = 0
articleSearches = 0


def home(request):

    context = {
        'pageName' : 'Home'
    }
    return render(request, 'webCred/home.html', context)


def jobListings(request):
    global jobSearches

    context = {
        'pageName' : 'Job Listing Check',
        'form' : jobForm(),
        'checkNum' : jobSearches
    }

    if request.method == 'POST':
        jobSearches += 1
        form = jobForm(request.POST)

        context.update({
                'form' : form,
                'isUpdated': True,
                'checkNum' : jobSearches
        })

        if form.is_valid():
            formParsed = []
            for category in form.cleaned_data:
                print(form.cleaned_data[category])
                formParsed.append(form.cleaned_data[category])
            preds = predictor.predictJob(*formParsed)

            context.update({
                    'isScam' : preds[0],
                    'confidence' : round(preds[1] * 100, 3)
            })

    return render(request, 'webCred/jobs.html', context)


def articles(request):
    global articleSearches

    context = {
        'pageName' : 'Articles',
        'form' : urlForm()
    }

    if request.method == 'POST':
        print(request.POST)

        articleSearches += 1
        form = urlForm(request.POST)
        context.update({
                'form' : form,
                'checkNum' : articleSearches
        })

        if 'articleName' in request.POST:
            formName = articleNameForm(request.POST)
            context.update({'formName' : formName})

            if formName.is_valid():
                articleName = formName.cleaned_data['articleName']
                preds = predictor.predictArticle(articleName)
                print(preds)
                context.update({
                        'isFake' : preds[0],
                        'confidence' : round(preds[1] * 100, 3),
                        'isUpdated' : True

                })


        else:
            if form.is_valid():
                url = form.cleaned_data['url']
                formName = articleNameForm()
                try:
                    #get HTML and convert into beautiful soup object
                    r = requests.get(url)
                    html_content = r.text
                    soup = BeautifulSoup(html_content, 'lxml')

                    formName.fields['articleName'].initial = soup.h1.string
                except:
                    formName.fields['articleName'].initial = "No Title Found"

                context.update({
                        'formName' : formName,
                        'isUpdated' : True
                })
            else:
                context.update({'errorMessage' : 'Invalid URL'})



    return render(request, 'webCred/article.html', context)
