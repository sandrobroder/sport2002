odoo.define('theme_clarico_vega.website_signup_ept', function(require) {
    'use strict';

    const {ReCaptcha} = require('google_recaptcha.ReCaptchaV3');
    var core = require('web.core');
    const session = require('web.session');
    const publicWidget = require('web.public.widget');
    const dom = require('web.dom');
    var _t = core._t;
    var ajax = require('web.ajax');

    publicWidget.registry.signupCaptchaVerificationOption = publicWidget.Widget.extend({
        selector: ".oe_signup_form",
        read_events: {
            "click button[type='submit']": "_onSignUpSubmit",
        },
        start: function() {
            this._super(...arguments);
        },
        init: function () {
            this._super(...arguments);
            this._recaptcha = new ReCaptcha();
//            this.orm = this.bindService("orm");
        },
        willStart: async function () {
            const res = this._super(...arguments);
            if (!this.el.classList.contains('form_no_recaptcha')) {
                this._recaptchaLoaded = true;
                this._recaptcha.loadLibs();
            }
            return res;
        },
        _onSignUpSubmit: async function (e) {
            e.preventDefault(); // Prevent the default submit behavior
             // Prevent users from crazy clicking
             const $button = this.$el.find('button[type="submit"]');
             $button.addClass('disabled') // !compatibility
                   .attr('disabled', 'disabled');
            this.restoreBtnLoading = dom.addButtonLoadingEffect($button[0]);

            var self = this;

            if (!self.check_error_fields({})) {
                if (this.fileInputError) {
                    const errorMessage = this.fileInputError.type === "number"
                        ? _t(
                            "Please fill in the form correctly. You uploaded too many files. (Maximum %s files)",
                            this.fileInputError.limit
                        )
                        : _t(
                            "Please fill in the form correctly. The file \"%s\" is too big. (Maximum %s MB)",
                            this.fileInputError.fileName,
                            this.fileInputError.limit
                        );
                    this.update_status("error", errorMessage);
                    delete this.fileInputError;
                } else {
                    this.update_status("error", _t("Please fill in the form correctly."));
                }
                return false;
            }

            // Prepare form inputs
            this.form_fields = this.$el.serializeArray();
            $.each(this.$el.find('input[type=file]:not([disabled])'), (outer_index, input) => {
                $.each($(input).prop('files'), function (index, file) {
                    // Index field name as ajax won't accept arrays of files
                    // when aggregating multiple files into a single field value
                    self.form_fields.push({
                        name: input.name + '[' + outer_index + '][' + index + ']',
                        value: file
                    });
                });
            });

            // Serialize form inputs into a single object
            // Aggregate multiple values into arrays
            var form_values = {};
            _.each(this.form_fields, function (input) {
                if (input.name in form_values) {
                    // If a value already exists for this field,
                    // we are facing a x2many field, so we store
                    // the values in an array.
                    if (Array.isArray(form_values[input.name])) {
                        form_values[input.name].push(input.value);
                    } else {
                        form_values[input.name] = [form_values[input.name], input.value];
                    }
                } else {
                    if (input.value !== '') {
                        form_values[input.name] = input.value;
                    }
                }
            });

            // force server date format usage for existing fields
            this.$el.find('.s_website_form_field:not(.s_website_form_custom)')
            .find('.s_website_form_date, .s_website_form_datetime').each(function () {
                const inputEl = this.querySelector('input');
                if (!inputEl.value) {
                    return;
                }

                var date = $(this).datetimepicker('viewDate').clone().locale('en');
                var format = 'YYYY-MM-DD';
                if ($(this).hasClass('s_website_form_datetime')) {
                    date = date.utc();
                    format = 'YYYY-MM-DD HH:mm:ss';
                }
                form_values[inputEl.getAttribute('name')] = date.format(format);
            });

            if (this._recaptchaLoaded) {
                const tokenObj = await this._recaptcha.getToken();
                if (tokenObj.token) {
                    form_values['recaptcha_token_response'] = tokenObj.token;
                } else if (tokenObj.error) {
                    self.update_status('error', tokenObj.error);
                    return false;
                }
            }

            /*call for the /web/signup and get the appropriate response and redirection value*/
            // Post form and handle result
            ajax.post('/web/signup', form_values)
            .then(async function (result_data) {
                    const login_data = JSON.parse(result_data)
                    var $error = $('.alert-success-error .alert-danger');
                    var $success = $('.alert-success-error .alert-success');
                    if (login_data.login_success && login_data.redirect) {
                        $error.addClass("d-none");
                        $success.removeClass("d-none");
                        window.location = '/web'
                    } else if (!login_data.login_success && login_data.error) {
                        $error.html('');
                        $error.removeClass("d-none").append(login_data.error);
                        $success.addClass("d-none");
                        $(".oe_signup_form .oe_login_buttons button").removeClass('disabled o_website_btn_loading').attr('disabled', false);
                        $(".oe_signup_form .oe_login_buttons button .fa-spin").removeClass('fa-refresh fa-spin');
                    }
            });
        },

        check_error_fields: function (error_fields) {
            var self = this;
            var form_valid = true;
            // Loop on all fields
            this.$el.find('.form-group').each(function (k, field) { // !compatibility
                var $field = $(field);
                // FIXME that seems broken, "for" does not contain the field
                // but this is used to retrieve errors sent from the server...
                // need more investigation.
                var field_name = $field.find('label').attr('for');

                // Validate inputs for this field
                var inputs = $field.find('.form-control, .form-check-input').not('#editable_select'); // !compatibility
                var invalid_inputs = inputs.toArray().filter(function (input, k, inputs) {
                    if (input.required && input.type === 'checkbox') {
                        var checkboxes = inputs.filter(input => input.required && input.type === 'checkbox');
                        return !checkboxes.some((checkbox) => checkbox.checkValidity());
                    }
                    return !input.checkValidity();
                });

                // Update field color if invalid or erroneous
                const $controls = $field.find('.form-control, .form-select, .form-check-input, .form-control-file');
                $field.removeClass('o_has_error');
                $controls.removeClass('is-invalid');
                if (invalid_inputs.length || error_fields[field_name]) {
                    $field.addClass('o_has_error');
                    $controls.addClass('is-invalid');
                    if (_.isString(error_fields[field_name])) {
                        $field.popover({content: error_fields[field_name], trigger: 'hover', container: 'body', placement: 'top'});
                        // update error message and show it.
                        const popover = Popover.getInstance($field);
                        popover._config.content = error_fields[field_name];
                        $field.popover('show');
                    }
                    form_valid = false;
                }
            });
            return form_valid;
        },

        update_status: function (status, message) {
            var $error = this.$('.alert-success-error .alert-danger'); // !compatibility
            if (status === 'error' && message) {
                $error.html('');
                $error.removeClass("d-none").append(message)
                this.restoreBtnLoading();
            }

        },
    });
});