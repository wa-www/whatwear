from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from .forms import CommentForm
from .models import Photo
from .models import Comment
from .models import Like
from whatwear import settings
from django.contrib import messages

#環境変数のため追記
import environ
# BASE_DIR = environ.Path(__file__) - 2
env = environ.Env()
env.read_env('.env')

import matplotlib.pyplot as plt
import cv2

# 天気情報のs取得
import requests
import json, pprint

from datetime import date
# from django.http import JsonResponse
from django.http.response import JsonResponse
import json

# def index(request):
#   return render(request,'photosend/index.html')

def index(request):
    # photos = Photo.objects.all().order_by('-created_at')
    # return render(request, 'photosend/index.html', {'photos': photos})

    if request.method=="POST":
          # APIキーの指定 - 以下を書き換えてください★ --- (※1)
      #環境変数に設定
      apikey=env('APIKEY')

      # 天気を調べたい都市の一覧 --- (※2)
      # if request.POST['city']:
      # cities = ["Tokyo,JP", "Osaka,JP", "Kyoto,JP"]
      city = request.POST.get('scity',False)
      # APIのひな型 --- (※3)
      api = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

      # 温度変換(ケルビン→摂氏) --- (※4)
      k2c = lambda k: k - 273.15

      # 各都市の温度を取得する --- (※5)
      # for name in cities:
          # APIのURLを得る --- (※6)
      url = api.format(city=request.POST['city'], key=apikey)
      # 実際にAPIにリクエストを送信して結果を取得する
      r = requests.get(url)
      # 結果はJSON形式なのでデコードする --- (※7)
      data = json.loads(r.text)

      # 結果を画面に表示 --- (※8)

      name=data["name"]
      d=data["dt"]
      weather=data["weather"][0]["description"]
      tempmin=(k2c(data["main"]["temp_min"]))
      tempmax=(k2c(data["main"]["temp_max"]))  
      return render(request, 'photosend/weather.html', {'city':name,'date':d,'weather':weather,'maxtemp':tempmax,'mintemp':tempmin})

      # result = {
      #   'city': data["name"],
      #   'date': data["dt"],
      #   'weather':data["weather"][0]["description"],
      #   'tempmax':(k2c(data["main"]["temp_max"])),
      #   'tempmin':(k2c(data["main"]["temp_min"]))

      #   }
      # # return JsonResponse(result)



    else:
      photos = Photo.objects.all().order_by('-created_at')
      today_photo=Photo.objects.filter(user=request.user.id, created_at__date=date.today()).last()
    return render(request, 'photosend/index.html', {'photos': photos, 'pic':today_photo})




@login_required
def photos_new(request):
  form=PhotoForm()
  today_all_photos=Photo.objects.filter(created_at__date=date.today())
  return render(request,'photosend/new.html',{'form':form, 'photos':today_all_photos})


@login_required
def create(request):
  if request.method=="POST":
    form = PhotoForm(request.POST,request.FILES)
    if form.is_valid():
      photo=form.save(commit=False)
      photo.user=request.user
      photo.save()
      messages.success(request, "投稿が完了しました！")
    return redirect('index')
  else:
    form=PhotoForm()
  return render(request,'photosend/new',{'form': form})

@login_required
def photo_detail(request, pk):
  # photo = get_object_or_404(Photo, id=pk)
  photo = Photo.objects.get(id=pk)
  comments = Comment.objects.filter(photo=pk)
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      photo_id = Photo.objects.get(id=pk)
      comment =form.save(commit=False)
      comment.user=request.user
      comment.photo=photo_id
      comment.save()
      return redirect('photosend:photo_detail', pk=pk)
    else:
      form = CommentForm()
    return render(request, 'photosend/photo_detail.html', {'photo': photo, 'form':form,  'comments':comments})
  else:
    form = CommentForm()
    return render(request, 'photosend/photo_detail.html', {'photo': photo, 'form':form,  'comments':comments})

@login_required
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    if request.method=="POST":
      form = PhotoForm(request.POST,instance=photo)
      if form.is_valid():
        form.save()
        return redirect('index')
    else:
       form = PhotoForm(instance=photo)
    return render(request, 'photosend/edit.html', {'form': form, 'photo':photo })

@login_required
def delete(request, pk):
    try:
      photo = Photo.objects.get(id=pk)
    except Photo.DoesNotExist:
      raise Http404
    photo.delete()
    return redirect('photosend:index')
    

def comment_delete(request, comment_pk):
    try:
      comment = Comment.objects.get(id=comment_pk)
      photo_id=comment.photo.id
    except Comment.DoesNotExist:
      raise Http404
    comment.delete()
    # photo = Predirecthoto.objects.get(id=comment.photo.id)
    return redirect('photosend:photo_detail', photo_id)
    # return render(request, 'photosend/photo_detail.html', {'pk':photo_id})


def user_index(request, user_pk):

    user_photos = Photo.objects.filter(user = user_pk).order_by('-created_at')
    return render(request, 'photosend/user_index.html', {'photos': user_photos})

@login_required
def edit_mosaic(request):

  # obj = Photo.objects.get()
  # max_id = Photo.objects.latest('id').id
  # obj = Photo.objects.get(id = max_id)


  if request.method=="POST":
    form = PhotoForm(request.POST,request.FILES)

    if form.is_valid() and 'button_gray' in request.POST:
      photo=form.save(commit=False)
      photo.user=request.user
      photo.save()

      max_id = Photo.objects.latest('id').id
      obj = Photo.objects.get(id = max_id)

      # active = Photo.objects.all()[0]
      active=settings.BASE_DIR + obj.photo.url
      # photo_path=active.path
      # photo_path=form.photo.path
        # カスケードファイルを指定して分類機を作成 
      # cascade_file = "/Users/noriko/p-projects/opencv-4.1.1/data/haarcascades/haarcascade_frontalface_alt.xml"
      cascade_file = "photosend/haarcascade_frontalface_alt.xml"
      cascade = cv2.CascadeClassifier(cascade_file)

      # 画像の読み込んでグレイスケールに変
      img = cv2.imread(active)
      img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      # 顔検出を実行 --- (*3)
      face_list = cascade.detectMultiScale(img_gray, minSize=(50,50))
      #物体認識（顔認識）の実行
      #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
      #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
      #scaleFactor – 各画像スケールにおける縮小量を表します
      #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
      #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
      #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
      
      # if len(face_list) == 0: quit()
      if len(face_list) == 0:
        return redirect('index')
      else:
      # 認識した部分の画像にモザイクをかける 
        for (x,y,w,h) in face_list:
          img = mosaic(img, (x, y, x+w, y+h), 10)

      #画像を出力
      cv2.imwrite(active, img)
      # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
      # plt.show()
      cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      cv2.imwrite(active, img)

      photo.save()
      messages.success(request, "投稿が完了しました！")
      return redirect('index')

    else:
      return render(request,'photosend/new',{'form': form})


def mosaic(img, rect, size):
    # モザイクをかける領域を取得
    (x1, y1, x2, y2) = rect
    w = x2 - x1
    h = y2 - y1
    i_rect = img[y1:y2, x1:x2]
    # 一度縮小して拡大する
    i_small = cv2.resize(i_rect, ( size, size))
    i_mos = cv2.resize(i_small, (w, h), interpolation=cv2.INTER_AREA)
    # 画像にモザイク画像を重ねる
    img2 = img.copy()
    img2[y1:y2, x1:x2] = i_mos
    return img2

def weather_get(request):
    # APIキーの指定 - 以下を書き換えてください★ 
  #環境変数に設定
  apikey=env('APIKEY')

  if request.POST['city']:
  # cities = ["Tokyo,JP", "Osaka,JP", "Kyoto,JP"]
    city = request.POST['city']
  api = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

  # 温度変換(ケルビン→摂氏)
  k2c = lambda k: k - 273.15
      # APIのURLを得る 
  url = api.format(city=request.POST['city'], key=apikey)
  # 実際にAPIにリクエストを送信して結果を取得する
  r = requests.get(url)
  # 結果はJSON形式なのでデコードする
  data = json.loads(r.text)

  # 結果を画面に表示 

  name=data["name"]
  date=data["dt"]
  weather=data["weather"][0]["description"]
  tempmin=(k2c(data["main"]["temp_min"]))
  tempmax=(k2c(data["main"]["temp_max"]))  


  # return render(request, 'index', {'city':name,'date':date,'weather':weather,'tempmax':tempmax,'tempmin':tempmin})

  result = {
    'city': name,
    'date': date,
    'weather':weather,
    'tempmax':tempmax,
    'tempmin':tempmin

    }
  return JsonResponse(result)


  # print("+ 都市=", data["name"])
  # print("+ 日付=", data["dt"])
  # print("| 天気=", data["weather"][0]["description"])
  # print("| 最低気温=", k2c(data["main"]["temp_min"]))
  # print("| 最高気温=", k2c(data["main"]["temp_max"]))
  # print("| 風速度=", data["wind"]["speed"])
  # print("")

@login_required
def like(request):
    # photo = Photo.objects.get(id=kwargs['post_id'])
    # photo = Photo.objects.get(id=pk)
    keyword=request.POST.get("photo_id",None)
    photo = Photo.objects.get(id=keyword)
    is_like = Like.objects.filter(user=request.user).filter(photo=photo.id).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(photo=photo.id, user=request.user)
        liking.delete()
        photo.like_num -= 1
        photo.save()
        result = {
        'num': photo.like_num,
        }
        return JsonResponse(result)
    # like
    photo.like_num += 1
    photo.save()
    like = Like()
    like.user = request.user
    like.photo = photo
    like.save()
    result = {
      'num': photo.like_num,
      }
    return JsonResponse(result)