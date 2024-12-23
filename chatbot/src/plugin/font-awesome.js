import { library } from '@fortawesome/fontawesome-svg-core';
import {
    faSearch,
    faPlus,
    faMagnifyingGlass,
    faChevronRight,
    faChevronDown,
    faChevronLeft,
    faScaleBalanced,
    faHouse
} from '@fortawesome/free-solid-svg-icons';
import { faCommentDots } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(
    faSearch,
    faPlus,
    faMagnifyingGlass,
    faChevronRight,
    faChevronDown,
    faCommentDots,
    faChevronLeft,
    faScaleBalanced,
    faHouse
);

export {FontAwesomeIcon};
