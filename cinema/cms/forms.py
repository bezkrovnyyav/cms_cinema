from .models import CarouselBanner, BackgroundBanner, HomePageBanner, PromotionsPageBanner, \
    Movies, Halls, Cinema, Events, ContactsPage, Page, HomePage, Images, SeoBlock, TemplatesMailing
from django.core.files.images import get_image_dimensions
from django import forms


# Forms for Banners

class CmsCarouselBannerForm(forms.ModelForm):
    """
    Form of carousel on HomePageBanner and PromotionsPageBanner
    """

    class Meta:
        model = CarouselBanner
        exclude = ('value',)

        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'interval': forms.Select(attrs={'class': 'form-control'})
        }


class CmsBackgroundBannerForm(forms.ModelForm):
    error_messages = {
        'error_banner': 'Размер изображения должен быть 2000x3000',
    }

    class Meta:
        model = BackgroundBanner
        exclude = ('value',)

        widgets = {
            'banner': forms.FileInput(attrs={'type': 'file',
                                             'onchange': "banner_valid(event)"}),
            'type': forms.RadioSelect()
        }

    def clean_banner(self):
        banner = self.cleaned_data['banner']
        if self.cleaned_data:
            width, height = get_image_dimensions(banner)
            if width != 3000 or height != 2000:
                raise forms.ValidationError(
                    self.error_messages['error_banner']
                )
        return banner


class CmsHomePageBannerForm(forms.ModelForm):
    error_messages = {
        'error_image': 'Размер изображения должен быть 1000x190',
    }

    class Meta:
        model = HomePageBanner
        fields = '__all__'

        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'}),
            'url': forms.URLInput(attrs={'class': 'form-control',
                                         'placeholder': 'Ссылка'}),
            'text': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'текст'})
        }

    def clean_image(self):
        images = self.cleaned_data['image']
        if self.cleaned_data:
            width, height = get_image_dimensions(images)
            if width != 1000 or height != 190:
                raise forms.ValidationError(
                    self.error_messages['error_image']
                )
        return images


class CmsPromotionsPageBannerForm(forms.ModelForm):
    error_messages = {
        'error_image': 'Размер изображения должен быть 1000x190',
    }

    class Meta:
        model = PromotionsPageBanner
        fields = '__all__'

        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'}),
            'url': forms.URLInput(attrs={'class': 'form-control',
                                         'placeholder': 'Ссылка'})
        }

    def clean_image(self):
        images = self.cleaned_data['image']
        if self.cleaned_data:
            width, height = get_image_dimensions(images)
            if width != 1000 or height != 190:
                raise forms.ValidationError(
                    self.error_messages['error_image']
                )
        return images


# Forms for Banners end


# Forms for Movies

class CmsMoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        exclude = ('gallery', 'seo_block')

        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название фильма'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"}),
            'link': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Ссылка на трейлер'}),
            'date_premier': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_3d': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                  'id': 'customCheckbox1'}),
            'type_2d': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                  'id': 'customCheckbox2'}),
            'type_imax': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                    'id': 'customCheckbox3'})

        }


# Forms for Movies end


# Forms for Halls

class CmsHallsForm(forms.ModelForm):
    class Meta:
        model = Halls
        exclude = ('gallery', 'seo_block', 'cinemas')

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control',
                                               'placeholder': 'Номер зала'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'banner': forms.FileInput(attrs={'type': 'file',
                                             'onchange': "document.getElementById('photo').src = window.URL.createObjectURL(this.files[0])"}),
            'layout': forms.FileInput(attrs={'type': 'file',
                                             'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"})
        }


# Forms for Halls end


# Forms for Cinemas

class CmsCinemasForm(forms.ModelForm):
    class Meta:
        model = Cinema
        exclude = ('gallery', 'seo_block', 'halls')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название кинотеатра'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                'placeholder': 'Условия'}),
            'photo': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('photo').src = window.URL.createObjectURL(this.files[0])"}),
            'logo': forms.FileInput(attrs={'type': 'file',
                                           'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"})
        }


# Forms for Cinemas end


# Forms for Events

class CmsEventsForm(forms.ModelForm):
    """
        Events Form for News and Promotions
    """

    class Meta:
        model = Events
        exclude = ('gallery', 'seo_block', 'type')

        widgets = {
            'is_published': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название'}),
            'date_published': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"}),

            'link': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Ссылка на видео в youtube'}),
        }


# Forms for Events end


# Forms for Pages


class CmsHomePageUpdateForm(forms.ModelForm):
    """
    Home Page Form
    """
    error_messages = {
        'error_phone_number': 'Неверный формат номера телефона',
    }

    class Meta:
        model = HomePage
        fields = ['phone_number1', 'phone_number2', 'active', 'seo_text']

        widgets = {
            'phone_number1': forms.TextInput(attrs={'class': 'form-control',
                                                    'data-mask': '000-00-00'}),
            'phone_number2': forms.TextInput(attrs={'class': 'form-control',
                                                    'data-mask': '000-00-00'}),
            'seo_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }

    def clean_phone_number1(self):
        phone_number1 = self.cleaned_data['phone_number1']
        if len(phone_number1) < 9:
            raise forms.ValidationError(
                self.error_messages['error_phone_number']
            )
        return phone_number1

    def clean_phone_number2(self):
        phone_number2 = self.cleaned_data['phone_number2']
        if len(phone_number2) < 9:
            raise forms.ValidationError(
                self.error_messages['error_phone_number']
            )
        return phone_number2


class CmsPageUpdateForm(forms.ModelForm):
    """
    Form for Pages
    """

    class Meta:
        model = Page
        exclude = ['seo_block', 'gallery', 'is_base']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'type': 'file',
                                            'onchange': "document.getElementById('logo').src = window.URL.createObjectURL(this.files[0])"})

        }


class CmsContactsPageUpdateForm(forms.ModelForm):
    """
    Contacts Page Form
    """

    class Meta:
        model = ContactsPage
        fields = ['title', 'address', 'active', 'coordinates', 'logo']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название кинотеатра'}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'placeholder': 'Адресс кинотеатра'}),
            'coordinates': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Координаты для карты'}),
            'logo': forms.FileInput(attrs={'type': 'file'})

        }


# Forms for Pages end

# Forms for mailing

class CmsTemplatesMailingForm(forms.ModelForm):
    TYPE_MAILING = [
        ('all', 'Все пользователи'),
        ('choice', 'Выборочно')
    ]
    type_mailing = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=TYPE_MAILING,
    )

    class Meta:
        model = TemplatesMailing
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={
                'type': 'file',
                'onchange': 'load_templates(this.files[0])'
            })
        }


# Forms for mailing end


# Forms related

class CmsImageForm(forms.ModelForm):
    """
    Image Form
    """
    error_messages = {
        'error_image': 'Размер изображения должен быть 1000x190'
    }

    class Meta:
        model = Images
        exclude = ('gallery',)

        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'})
        }

    def clean_image(self):
        images = self.cleaned_data['image']
        if self.cleaned_data:
            width, height = get_image_dimensions(images)
            if width != 1000 or height != 190:
                raise forms.ValidationError(
                    self.error_messages['error_image']
                )
        return images


class CmsSeoBlockForm(forms.ModelForm):
    """
    Seo Block Form
    """
    error_messages = {
        'keywords': 'error_messages'
    }

    class Meta:
        model = SeoBlock
        fields = '__all__'

        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control',
                                         'placeholder': 'url'}),
            'title_seo': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'title'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'keywords'}),
            'description_seo': forms.Textarea(attrs={'class': 'form-control',
                                                     'rows': 3,
                                                     'placeholder': 'description'})
        }

# Forms related end
