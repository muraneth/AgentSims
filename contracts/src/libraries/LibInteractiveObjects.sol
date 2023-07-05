// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

library LibInteractiveObjects {
    struct InteractiveObject {
        string name;
        int32 x;
        int32 y;
        int32 width;
        int32 height;
    }

    function getAllInteractiveObjects() internal pure returns (InteractiveObject[] memory) {
        InteractiveObject[] memory allInteractiveObjects = new InteractiveObject[](11);
        allInteractiveObjects[0] = InteractiveObject('Instrument', 19, 33, 4, 3);
        allInteractiveObjects[1] = InteractiveObject('Temple gate', 72, 37, 3, 2);
        allInteractiveObjects[2] = InteractiveObject('Instrument', 130, 34, 4, 4);
        allInteractiveObjects[3] = InteractiveObject('Pavilion', 13, 30, 5, 6);
        allInteractiveObjects[4] = InteractiveObject('Pavilion', 125, 36, 4, 3);
        allInteractiveObjects[5] = InteractiveObject('Pavilion', 134, 36, 4, 3);
        allInteractiveObjects[6] = InteractiveObject('Pavilion', 134, 31, 3.0, 3);
        allInteractiveObjects[7] = InteractiveObject('Pavilion', 125, 31, 3.0, 3);
        allInteractiveObjects[8] = InteractiveObject('Church gate', 10, 57, 2, 2);
        allInteractiveObjects[9] = InteractiveObject('Speaker', 136, 51, 4, 3);
        allInteractiveObjects[10] = InteractiveObject('Speaker', 126, 60, 1, 3);
        return allInteractiveObjects;
    }
}