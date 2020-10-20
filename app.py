#-*-coding:utf-8-*-
from flask import Flask, render_template, flash, request
from wtforms import Form, SelectField, validators, IntegerField
 

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            #'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
class ReusableForm(Form):
    first_thresh = IntegerField('first_thresh', validators=[validators.required()])
    morph        = IntegerField('morph', validators=[validators.required()])
    border_size  = IntegerField('border_size', validators=[validators.required()])
    gap          = IntegerField("gap", validators=[validators.required()])
    template     = SelectField(u'template', choices=[('cv2.TM_CCOEFF', 'cv2.TM_CCOEFF'), ('cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCOEFF_NORMED'), ('cv2.TM_CCORR', 'cv2.TM_CCORR'),
                                                               ('cv2.TM_CCORR_NORMED', 'cv2.TM_CCORR_NORMED'), ('cv2.TM_SQDIFF', 'cv2.TM_SQDIFF'), ('cv2.TM_SQDIFF_NORMED', 'cv2.TM_SQDIFF_NORMED')])
    sec_thresh   = IntegerField('sec_thresh', validators=[validators.required()])
    abs_distance = IntegerField('abs_distance', validators=[validators.required()])
    display      = SelectField(u'display', choices=[('1', '1'), ('0', '0')])
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        try:
            first_thresh = request.form['first_thresh']
            morph        = request.form['morph']
            gap          = request.form['gap']
            template     = request.form['template']
            sec_thresh   = request.form['sec_thresh']
            abs_distance = request.form['abs_distance']
            border_size  = request.form['border_size']
            display      = request.form['display']
            check1 = 0  <= int(first_thresh) <= 255
            check2 = 0  <= int(morph)        <= 10
            check3 = 30 <= int(gap)          <= 70
            check4 = 0  <= int(sec_thresh)   <= 255
            check5 = 1  <= int(abs_distance) <= 6
            check6 = 0  <= int(border_size)  <= 80
        except ValueError as err:
            pass


        if form.validate() and check1 and check2 and check3 and check4 and check5 and check6:
            flash('First Thresh: ' + first_thresh)
            flash('Morph: ' + morph)
            flash('Gap: ' + gap)
            flash('Template: ' + template)
            flash('Second Thresh: ' + sec_thresh)
            flash('Abs Distance: ' + abs_distance)
            flash('Border Size :' + border_size)
            flash('Display :' + display)
            file = open('webvalues.txt', 'w')
            file.write("<first_th>{}</first_th>\n".format(int(first_thresh)))
            file.write("<morph>{}</morph>\n".format(int(morph)))
            file.write("<gap>{}</gap>\n".format(int(gap)))
            file.write("<template>{}</template>\n".format(template))
            file.write("<second_th>{}</second_th>\n".format(int(sec_thresh)))
            file.write("<abs_distance>{}</abs_distance>\n".format(int(abs_distance)))
            file.write("<border_size>{}</border_size>\n".format(int(border_size)))
            file.write("<display>{}</display>\n".format(int(display)))
            file.close()



        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)
 
if __name__ == "__main__":
    app.run()
