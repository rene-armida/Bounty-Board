// jasmine tests for bounty.js


describe("HackListItem tests", function() {

	it("renders to an LI", function() {
		function MockHack() {
			this.name = 'hack name'
			this.abstract = 'hack abstract'
			this.toJSON = function() {
				return this;
			}
		}

		item = new window.bounty.HackListItemView({
			model: new MockHack, 
		})
		item.render()

		console.log('hi')
		expect(item.el.innerHTML).toContain("<h2>hack name</h2>");
		expect(item.el.innerHTML).toContain("<p>hack abstract</p>");

	});

});