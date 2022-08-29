import smartpy as sp

class CrowdFund(sp.Contract):
  def __init__(self):
    self.init(
      causes=sp.big_map(
        tkey=sp.TNat, 
        tvalue=sp.TRecord(
          owner=sp.TAddress, 
          cause_title=sp.TString,
          balance=sp.TMutez
        )
      ),
      fundings=sp.big_map(
        tkey=sp.TRecord(
          cause_id=sp.TNat,
          funder=sp.TAddress
        ),
        tvalue=sp.TMutez
      )
    )

  @sp.entry_point
  def create_cause(self, cause_id, title):
    """ Creates a new cause. """
    # Sanity checks or Assertions (Verify if the cause_id doesn't exists )
    sp.verify(~ self.data.causes.contains(cause_id))
    self.data.causes[cause_id] = sp.record(owner=sp.sender, cause_title=title , balance=sp.mutez(0))
  
  @sp.entry_point
  def fund_cause(self, cause_id):
    """ Funds a specific cause """
    # Sanity checks or Assertions (Verify if the cause_id exists)
    sp.verify(self.data.causes.contains(cause_id))

    # Storage updates
    self.data.fundings[sp.record(cause_id=cause_id, funder=sp.sender)] = sp.amount
    self.data.causes[cause_id].balance += sp.amount
  
  @sp.entry_point
  def withdraw_funds(self, cause_id):
    """ It allows the owner of a cause to transfer withdraw the funds. """
    # Sanity checks or Assertions (Verify if the cause_id exists)
    sp.verify(self.data.causes.contains(cause_id))
    # Sanity checks or Assertions (Verify if the sender/reciever is the owner of the cause)
    sp.verify(self.data.causes[cause_id].owner == sp.sender)

    # Transfer the collected funds
    sp.send(self.data.causes[cause_id].owner, self.data.causes[cause_id].balance)

    # Storage updates (Reset the amount as it's withdrawn now.)
    self.data.causes[cause_id].balance = sp.mutez(0)


@sp.add_test("Social Block")
def test():
  """ Test for our smart contract. """
  scenario = sp.test_scenario()
  # Contract instance 
  social = CrowdFund()
  
  owner = sp.test_account("Owner")
  Person1 = sp.test_account("Person1")
  Person2 = sp.test_account("Person2")

   # adding instance into scenario
  scenario += social
  scenario.h2("Create the cause(Valid Test)")
  scenario += social.create_cause(cause_id=1, title="Test").run(sender=owner)

  
  scenario.h2("Funding the Cause (valid test)")
  # Now funding the cause
  scenario += social.fund_cause(1).run(sender=Person1, amount=sp.mutez(2000000))
  scenario += social.fund_cause(1).run(sender=Person2, amount=sp.mutez(1000000))
  

  scenario.h2("Verifying the Amount (valid test)")
  # verify the amount
  scenario.verify(social.data.causes[1].balance == sp.mutez(3000000))
  
  # Should raise an error
  scenario += social.create_cause(cause_id=1, title="Just for fun Test").run(sender=owner, valid=False)
  
  
  # Withdrawing funds 
  # Should raise error 
  scenario += social.withdraw_funds(1).run(sender=Person1, valid=False)
  scenario += social.create_cause(cause_id=2, title="Education").run(sender=owner)
  
  scenario.h2("WithDrawn owner (valid test)")
  # With correct owner
  scenario += social.withdraw_funds(1).run(sender=owner)
  