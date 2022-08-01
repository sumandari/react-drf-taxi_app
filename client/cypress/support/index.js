import 'cypress-file-upload';

const addUser = (email, firstName, lastName, userType) => {
  cy.intercept('POST', 'sign_up').as('signUp');

  cy.visit('/#/sign-up');
  cy.get('input#username').type(email);
  cy.get('input#firstName').type(firstName);
  cy.get('input#lastName').type(lastName);
  cy.get('input#password').type('password', { log: false });
  cy.get('select#group').select(userType);

  cy.get('input#photo').attachFile('images/photo.jpg');

  cy.get('button').contains('Sign up').click();
  cy.wait('@signUp');
  cy.hash().should('eq', '#/log-in');
};

const logIn = (email) => { 
  cy.intercept('POST', 'log_in').as('logIn');
  cy.visit('/#/log-in');
  cy.get('input#username').type(email);
  cy.get('input#password').type('password', { log: false });
  cy.get('button').contains('Log in').click();
  cy.wait('@logIn');
}

Cypress.Commands.add('addUser', addUser);
Cypress.Commands.add('logIn', logIn);