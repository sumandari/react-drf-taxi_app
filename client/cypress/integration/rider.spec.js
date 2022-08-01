const faker = require('faker');

const driverEmail = faker.internet.email();
const riderEmail = faker.internet.email();
const driverFirstName = faker.name.firstName();
const riderFirstName = faker.name.firstName();
const driverLastName = faker.name.lastName();
const riderLastName = faker.name.lastName();


describe('The rider dashboard', function () {
  before(function () {
    cy.addUser(riderEmail, riderFirstName, riderLastName, 'rider');
    cy.addUser(driverEmail, driverFirstName, driverLastName, 'driver');
  });

  it('Cannot be visited if the user us not a rider', function () {
    cy.intercept('POST', 'sign_up').as('signUp');
    cy.intercept('POST', 'log_in').as('logIn');

    cy.logIn(driverEmail);

    cy.visit('/#/rider');
    cy.hash().should('eq', '#/');
  });

  it('Can be visited if the user is a rider', function () {
    cy.intercept('POST', 'sign_up').as('signUp');
    cy.intercept('POST', 'log_in').as('logIn');

    cy.logIn(riderEmail);

    cy.visit('/#/rider');
    cy.hash().should('eq', '#/rider');
  });
});