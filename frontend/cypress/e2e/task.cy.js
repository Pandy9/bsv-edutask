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
        
    cy.get('div.container-element a')
    .last()
    .click()
})
    it('Create a new todo item WITH a description and then delete it', () => {
    // Add the todo item
    cy.contains('div.popup', taskTitle)
        .should('contain.text', taskTitle)
        .find('form')
        .find('input[type=text]')
        .type(todoTitle)

    cy.contains('div.popup', taskTitle)
        .find('form.inline-form')
        .submit()

    // Assert todo item exists
    cy.contains('li.todo-item', todoTitle).should('exist')
    })

    it('Should not allow creating a todo item WITHOUT a description', () => {
    cy.contains('div.popup', taskTitle)
        .should('contain.text', taskTitle)
        .find('form.inline-form')
        .within(() => {
  
        cy.get('input[type=submit]')
            .should('be.disabled')
        })
    })
    it('Should delete a todo item and assert it is removed', () => {
    // Ensure popup is open with the right task title
    cy.contains('div.popup', taskTitle)
        .should('contain.text', taskTitle)
        .within(() => {
        // Find the last todo-item and click its delete button (span.remover)
        cy.get('ul.todo-list')
            .find('li.todo-item')
            .last()
            .find('span.remover')
            .click()
        })

    // Assert that the todo-item with the specific title no longer exists
    cy.contains('div.popup', taskTitle)
        .find('ul.todo-list')
        .find('li.todo-item')
        .contains(todoTitle)
        .should('not.exist')
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

