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
	tagName: 'ul',
	id: 'hacklist',

	initialize: function() {
		this.model.bind("reset", this.render, this);
	},

	render: function(eventName) {
		_.each(this.model.models, function(hack) {
			// pass detailView down to list item views
			this.$el.append(new window.bounty.HackListItemView({model:hack, detailView: this.options.detailView}).render().el);
		}, this);
		return this;
	}
})

window.bounty.HackListItemView = Backbone.View.extend({
	tagName: 'li',
	template: '<h2>{{ name }}</h2><p>{{ abstract }}</p>',

	render: function(eventName) {
		this.$el.html(Mustache.render(this.template, this.model.toJSON()))
		return this
	},

	highlight: function() {
		// unhighlight any previously-highlighted elements
		$('.highlight').removeClass('highlight')

		// style the element
		this.$el.addClass('highlight')

		// poke the detail view into refreshing
		this.options.detailView.newSelection(this.model)
	},

	events: {
		"click": "highlight",
	},
})

window.bounty.HackDetailView = Backbone.View.extend({
	tagName: 'div',
	template: '\
		<h2>{{ name }}</h2> \
		<h3>{{ abstract }}</h3> \
		<p>{{{ description }}}</p> \
		\
		<div class="credits"> \
			<p><span>Proposed by:</span> <a href="#user/{{author.username}}">{{author.username}}</a></p>\
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
		converter = new Markdown.Converter();
		view.description = converter.makeHtml(view.description)
		this.$el.html(Mustache.render(this.template, view))
		
		return this
	},

	newSelection: function(hack) {
		this.model = hack
		this.render()
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
		},

		list: function() {
			// create the detail view and hang on to a reference to it
			this.hackDetailView = new window.bounty.HackDetailView({el: $('#rcol')})
			
			this.hackList = new window.bounty.HackCollection()
			// provide detail view to hack list, so it can communicate with it when the selection changes
			this.hackListView = new window.bounty.HackListView({model: this.hackList, detailView: this.hackDetailView})
			this.hackList.fetch()
			$('#lcol').append(this.hackListView.render().el);

		},

		profile: function(username) {
			// show a user's details and related hacks
			alert('AppRouter#profile: implement me')
		},

		tag: function(tagname) {
			// show hacks associatde with a tag
			alert('AppRouter#tag: implement me')
		}
	})

	// run it
	var app = new AppRouter()
	Backbone.history.start()
}