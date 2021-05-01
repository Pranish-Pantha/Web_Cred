from django.http import HttpResponse
from django.shortcuts import render
from .forms import urlForm, jobForm, articleNameForm
from .networkPreds import predictorNLP
import requests
from bs4 import BeautifulSoup
from django.views.generic import TemplateView, View

predictor = predictorNLP()
articleSearches = 0

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageName'] = 'Home'
        return context
class JobListingView(View):
    context = {'pageName' : 'Job Listing Check', 'checkNum': 0}

    def get(self, *args, **kwargs):
        self.context['form'] = jobForm()
        return render(self.request, 'jobs.html', self.context)
    def post(self, *args, **kwargs):
        self.context['checkNum'] += 1
        form = jobForm(self.request.POST)
        self.context.update({
                'form' : form,
                'isUpdated': True,
        })

        if form.is_valid():
            formParsed = []
            for category in form.cleaned_data:
                print(form.cleaned_data[category])
                formParsed.append(form.cleaned_data[category])
            preds = predictor.predictJob(*formParsed)

            self.context.update({
                    'isScam' : preds[0],
                    'confidence' : round(preds[1] * 100, 3)
            })
        return render(self.request, 'jobs.html', self.context)
class ArticlesView(View):
    context = { 'pageName' : 'Articles', 'checkNum': 0}
    def get(self, *args, **kwargs):
        self.context['form'] = urlForm()
        return render(self.request, 'article.html', self.context)

    def post(self, *args, **kwargs):
        self.context['checkNum'] += 1
        form = urlForm(self.request.POST)
        self.context.update({
                'form' : form,
        })
        if 'articleName' in self.request.POST:
            formName = articleNameForm(self.request.POST)
            self.context.update({'formName' : formName})

            if formName.is_valid():
                articleName = formName.cleaned_data['articleName']
                preds = predictor.predictArticle(articleName)
                print(preds)
                self.context.update({
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

                self.context.update({
                        'formName' : formName,
                        'isUpdated' : True
                })
            else:
                self.context.update({'errorMessage' : 'Invalid URL'})
        return render(self.request, 'article.html', self.context)
