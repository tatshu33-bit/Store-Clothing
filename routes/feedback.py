from flask import Blueprint, render_template, request, redirect, url_for, flash
import models

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name') or 'Анонім'
        email = request.form.get('email')
        message = request.form.get('message')
        if not message:
            flash('Повідомлення не може бути порожнім', 'danger')
            return redirect(url_for('feedback.feedback'))
        models.add_feedback(name, email, message)
        flash('Дякуємо! Ваш відгук надіслано.', 'success')
        return redirect(url_for('feedback.feedback'))
    feedbacks = models.get_feedbacks()
    return render_template('feedback.html', feedbacks=feedbacks)
