from flask import render_template, redirect, url_for, flash, request
from app.admin.forms import UserForm
from app.models import User
from app import db

@admin_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            balance=form.balance.data,
            commission_rate=form.commission_rate.data,
            webhook_url=form.webhook_url.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)
