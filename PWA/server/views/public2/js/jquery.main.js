jQuery(function() {
  initMobileNav();
  initFocusClass();
});


// mobile menu init
function initMobileNav() {
  jQuery('body').mobileNav({
    menuActiveClass: 'nav-active',
    menuOpener: '.nav-opener',
    hideOnClickOutside: true,
    menuDrop: '#nav, .user-nav'
  });
}

// add class when element is in focus
function initFocusClass() {
  /*jQuery('.form-group').addFocusClass({
    focusClass: 'input-focused',
    element: '.form-control',
    stayFocusOnFilled: true
  });*/
}


/*
 * Simple Mobile Navigation
 */
;(function($) {
  function MobileNav(options) {
    this.options = $.extend({
      container: null,
      hideOnClickOutside: false,
      menuActiveClass: 'nav-active',
      menuOpener: '.nav-opener',
      menuDrop: '.nav-drop',
      toggleEvent: 'click',
      outsideClickEvent: 'click touchstart pointerdown MSPointerDown'
    }, options);
    this.initStructure();
    this.attachEvents();
  }
  MobileNav.prototype = {
    initStructure: function() {
      this.page = $('html');
      this.container = $(this.options.container);
      this.opener = this.container.find(this.options.menuOpener);
      this.drop = this.container.find(this.options.menuDrop);
    },
    attachEvents: function() {
      var self = this;

      if(activateResizeHandler) {
        activateResizeHandler();
        activateResizeHandler = null;
      }

      this.outsideClickHandler = function(e) {
        if(self.isOpened()) {
          var target = $(e.target);
          if(!target.closest(self.opener).length && !target.closest(self.drop).length) {
            self.hide();
          }
        }
      };

      this.openerClickHandler = function(e) {
        e.preventDefault();
        self.toggle();
      };

      this.opener.on(this.options.toggleEvent, this.openerClickHandler);
    },
    isOpened: function() {
      return this.container.hasClass(this.options.menuActiveClass);
    },
    show: function() {
      this.container.addClass(this.options.menuActiveClass);
      if(this.options.hideOnClickOutside) {
        this.page.on(this.options.outsideClickEvent, this.outsideClickHandler);
      }
    },
    hide: function() {
      this.container.removeClass(this.options.menuActiveClass);
      if(this.options.hideOnClickOutside) {
        this.page.off(this.options.outsideClickEvent, this.outsideClickHandler);
      }
    },
    toggle: function() {
      if(this.isOpened()) {
        this.hide();
      } else {
        this.show();
      }
    },
    destroy: function() {
      this.container.removeClass(this.options.menuActiveClass);
      this.opener.off(this.options.toggleEvent, this.clickHandler);
      this.page.off(this.options.outsideClickEvent, this.outsideClickHandler);
    }
  };

  var activateResizeHandler = function() {
    var win = $(window),
      doc = $('html'),
      resizeClass = 'resize-active',
      flag, timer;
    var removeClassHandler = function() {
      flag = false;
      doc.removeClass(resizeClass);
    };
    var resizeHandler = function() {
      if(!flag) {
        flag = true;
        doc.addClass(resizeClass);
      }
      clearTimeout(timer);
      timer = setTimeout(removeClassHandler, 500);
    };
    win.on('resize orientationchange', resizeHandler);
  };

  $.fn.mobileNav = function(opt) {
    var args = Array.prototype.slice.call(arguments);
    var method = args[0];

    return this.each(function() {
      var $container = jQuery(this);
      var instance = $container.data('MobileNav');

      if (typeof opt === 'object' || typeof opt === 'undefined') {
        $container.data('MobileNav', new MobileNav($.extend({
          container: this
        }, opt)));
      } else if (typeof method === 'string' && instance) {
        if (typeof instance[method] === 'function') {
          args.shift();
          instance[method].apply(instance, args);
        }
      }
    });
  };
}(jQuery));

/*
 * Add Class on focus
 */
;(function($) {
  function AddFocusClass(options) {
    this.options = $.extend({
      container: null,
      element: ':input',
      focusClass: 'focus',
      stayFocusOnFilled: false
    }, options);
    this.initStructure();
    this.attachEvents();
  }
  AddFocusClass.prototype = {
    initStructure: function() {
      this.container = $(this.options.container);
      this.element = this.container.find(this.options.element);
    },
    attachEvents: function() {
      var self = this;
      this.focusHandler = function() {
        self.container.addClass(self.options.focusClass);
      };
      this.blurHandler = function() {
        if (self.options.stayFocusOnFilled) {
          self.container.toggleClass(self.options.focusClass, !!self.element.val().trim().length);
        } else {
          self.container.removeClass(self.options.focusClass);
        }
      };
      this.blurHandler();
      this.element.on({
        focus: this.focusHandler,
        blur: this.blurHandler
      });
    },
    destroy: function() {
      this.container.removeClass(this.options.focusClass);
      this.element.off({
        focus: this.focusHandler,
        blur: this.blurHandler
      });
    }
  };

  $.fn.addFocusClass = function(options) {
    return this.each(function() {
      var params = $.extend({}, options, {
          container: this
        }),
        instance = new AddFocusClass(params);
      $.data(this, 'AddFocusClass', instance);
    });
  };
}(jQuery));

