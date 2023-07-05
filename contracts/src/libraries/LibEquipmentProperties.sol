// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library LibEquipmentProperties {

    struct EquipmentProperties {
        string name;
        string description;
        string[] operations;
    }

    function getAllObjectTypes1() internal pure returns (EquipmentProperties[] memory) {
        EquipmentProperties[] memory objectTypes = new EquipmentProperties[](6);

        objectTypes[0] = EquipmentProperties("bed", "You can sleep with a bed.", new string[](1));
        objectTypes[0].operations[0] = "sleep";

        objectTypes[1] = EquipmentProperties("tv", "You can watch tv with a tv.", new string[](1));
        objectTypes[1].operations[0] = "watch";

        objectTypes[2] = EquipmentProperties("dinner table", "You can have meal with a dinner table.", new string[](1));
        objectTypes[2].operations[0] = "have meal";

        objectTypes[3] = EquipmentProperties("kitchen", "You can make a meal with a kitchen.", new string[](1));
        objectTypes[3].operations[0] = "make a meal";

        objectTypes[4] = EquipmentProperties("restaurant counter", "You can buy a meal with a bar counter.", new string[](1));
        objectTypes[4].operations[0] = "buy a meal";

        objectTypes[5] = EquipmentProperties("cafe seat", "You can drink coffee with a cafe seat.", new string[](1));
        objectTypes[5].operations[0] = "drink coffee";

        return objectTypes;
    }

    function getAllObjectTypes2() internal pure returns (EquipmentProperties[] memory) {
        EquipmentProperties[] memory objectTypes = new EquipmentProperties[](6);

        objectTypes[0] = EquipmentProperties("cafe counter", "You can buy coffee with a cafe counter.", new string[](1));
        objectTypes[0].operations[0] = "buy coffee";

        objectTypes[1] = EquipmentProperties("bar seat", "You can drink wine with a bar seat.", new string[](1));
        objectTypes[1].operations[0] = "drink wine";

        objectTypes[2] = EquipmentProperties("bar counter", "You can buy wine with a bar counter.", new string[](1));
        objectTypes[2].operations[0] = "buy wine";

        objectTypes[3] = EquipmentProperties("rest room", "You can rest with a rest room.", new string[](1));
        objectTypes[3].operations[0] = "rest";

        objectTypes[4] = EquipmentProperties("office seat", "You can work with a office seat if you are a worker.", new string[](1));
        objectTypes[4].operations[0] = "work";

        objectTypes[5] = EquipmentProperties("school class", "You can teach students with a school class if you are a teacher.", new string[](1));
        objectTypes[5].operations[0] = "teach students";

        return objectTypes;
    }
}
