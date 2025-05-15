describe('Testing the task management system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let taskTitle = 'Test task'
  let todoTitle = 'Test todo item'

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email

          cy.visit('http://localhost:3000')
          cy.contains('div', 'Email Address').type(email)
            cy.get('form')
                .submit()
          cy.contains('div', 'Title')
            .find('input[type=text]').type(taskTitle)
          cy.contains('div', 'YouTube URL')
            .find('input[type=text]').type('http://www.youtube.com/watch?v=dQw4w9WgXcQ')
          cy.get('form')
            .submit()
        })
      })
  })
  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address').type(email)
        cy.get('form')
            .submit()
        
    cy.contains('div', taskTitle).click()
  })
  it('starting out on the landing screen', () => {
    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})

