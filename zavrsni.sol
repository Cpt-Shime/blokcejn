// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Zavrsni {
    address public owner;
    string public name;
    uint256 public totalSupply;
    mapping (address => uint256) public balances;

    constructor(string memory _name, uint256 _totalSupply) public {
        owner = msg.sender;
        name = _name;
        totalSupply = _totalSupply;
        balances[msg.sender] = totalSupply;
    }

    modifier onlyOwner() {
            require(msg.sender == owner, "Samo vlasnik može pozvat.");
            _;
    }

    function checkBalanceOf(address _owner) public view returns (uint256) {
            return balances[_owner];
    }


    function transfer(address _to, uint256 _value) public returns (bool success) {
            require(balances[msg.sender] >= _value, "Nedovoljno soldi.");
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            return true;
    }

    function mint(uint256 _amount) public onlyOwner {
        totalSupply += _amount;
        balances[owner] += _amount;

    }

    function burn(uint256 _amount) public onlyOwner {
            require(balances[owner] >= _amount, "Nedovoljno soldi.");
            totalSupply -= _amount;
            balances[owner] -= _amount;
    }
}