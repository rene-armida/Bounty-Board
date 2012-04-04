// a little bit of namespacing
// todo: is there a better way to do this?
window.bounty = {}

// models
window.bounty.Hack = Backbone.Model.extend({
	schema: {
		name: {},
		abstract: {},
		description: {},
	},
})

// collections
window.bounty.HackCollection = Backbone.Collection.extend({
	model: window.bounty.Hack,
	url: '/api/hacks',
})

// views
window.bounty.HackListView = Backbone.View.extend({
	tagName: 'div',
	template: '\
		<h1>Hacks</h1> \
		<ul id="hacklist"></ul>',

	initialize: function() {
		this.model.bind("reset", this.render, this)
	},

	render: function(eventName) {
		this.$el.html(this.template)

		ul = this.$el.find('#hacklist')
		_.each(this.model.models, function(hack) {
			ul.append(new window.bounty.HackListItemView({model:hack}).render().el)
		}, this)

		this.$el.find('h1').before(new window.bounty.HackListControlsView().render().el)

		return this
	}
})

window.bounty.HackListControlsView = Backbone.View.extend({
	tagName: 'div',
	className: 'controls',
	template: '\
		<select name=""><option>All</option><option>Most popular</option><option>Next Meetup</option></select> \
		<button>New</button>',

	render: function(eventName) {
		this.$el.html(this.template)
		return this
	}

})

window.bounty.HackControlsView = Backbone.View.extend({
	tagName: 'div',
	className: 'controls',
	template: '\
		<button>Like ({{numLike}})</button> \
		<button>Pledge ({{numPledged}})</button> \
		',
	render: function(eventName) {
		// todo: correct like and pledge counts
		this.$el.html(Mustache.render(this.template, {numLike: 0, numPledged: 0}))
		return this
	}
})

window.bounty.HackListItemView = Backbone.View.extend({
	tagName: 'li',
	template: '\
		<h2><a href="#hack/{{id}}">{{ name }}</a></h2>\
		<p>By <a href="#user/{{author.username}}">{{author.first_name}} {{author.last_name}}</a></p>\
		<p>{{ abstract }}</p>',

	render: function(eventName) {
		this.$el.html(Mustache.render(this.template, this.model.toJSON()))
		var controls = new window.bounty.HackControlsView({model: this.model})
		this.$el.find('h2').before(controls.render().el)
		return this
	},

	hack_url: function() {
		// todo: add slug
		return 'hack/' + this.model.get('id')
	},

	trigger_detail: function() {
		window.bounty.app.navigate(this.hack_url(), {trigger: true})
	},

	events: {
		"click": "trigger_detail",
	},
})

window.bounty.HackDetailView = Backbone.View.extend({
	tagName: 'div',
	className: 'detail',
	template: '\
		<h2>{{ name }}</h2> \
		<h3>{{ abstract }}</h3> \
		<p>{{{ description }}}</p> \
		\
		<div class="credits"> \
			<p><span>Proposed by:</span> <a href="#user/{{author.username}}">{{author.username}}</a> \
				<span>On:</span> {{created}} \
			</p>\
			<p><span>Contributors: </span> \
				{{#contributors}} \
					<a href="#user/{{username}}">{{author.name}}</a> \
				{{/contributors}} \
			</p>\
			<p><span>Liked by: </span> \
				{{#liked_by}} \
					<a href="#user/{{username}}">{{author.name}}</a> \
				{{/liked_by}} \
			</p>\
		</div>\
		\
		<p><span>Tagged:</span> \
		{{#tags}}\
			<a href="#tag/{{slug}}">{{name}}</a>&nbsp;&nbsp; \
		{{/tags}}\
		</p>',

	render: function(eventName) {
		view = this.model.toJSON()
		// todo: make this generic, so not every rendering function needs to implement their own call to Markdown.Converter
		// todo: add markdown sanitizer
		var converter = new Markdown.Converter()
		view.description = converter.makeHtml(view.description)
		this.$el.html(Mustache.render(this.template, view))

		var controls = new window.bounty.HackControlsView({model: this.model})
		this.$el.find('h2').before(controls.render().el)
		
		return this
	},
})

window.bounty.HackEditView = Backbone.View.extend({
	render: function() {
		var form = new Backbone.Form({
			model: new window.bounty.Hack(),
		}).render()

		this.$el.append(form.el)
		return this
	},
})

// hooks for invocation by django templates
window.bounty.home_view = function() {
	// routes
	var AppRouter = Backbone.Router.extend({
		routes: {
			'': 'list',
			'user/:username': 'profile',
			'tag/:tagname': 'tag',
			'hack/:id': 'hack_detail',
		},

		initialize: function() {
			this.hackList = new window.bounty.HackCollection()
			this.hackList.fetch()
		},

		list: function() {
			this.hackListView = new window.bounty.HackListView({model: this.hackList})
			$('#content').empty().append(this.hackListView.render().el);
		},

		profile: function(username) {
			// show a user's details and related hacks
			alert('AppRouter#profile: implement me')
		},

		tag: function(tagname) {
			// show hacks associatde with a tag
			alert('AppRouter#tag: implement me')
		},

        hack_detail: function(id) {
            // show the details of one hack
            this.hackDetailView = new window.bounty.HackDetailView({model: this.hackList.get(id)})
            $('#content').empty().append(this.hackDetailView.render().el)
        },
	})

	// run it
	window.bounty.app = new AppRouter()
	Backbone.history.start()
}