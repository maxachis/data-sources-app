import { createWebHistory, createRouter } from 'vue-router';
import QuickSearchPage from '../src/pages/QuickSearchPage';
import SearchResultPage from '../src/pages/SearchResultPage';
import AdvancedSearchPage from '../src/pages/AdvancedSearchPage';

const routes = [
	{ path: '/', component: QuickSearchPage, name: 'QuickSearchPage' },
	{
		path: '/search/:searchTerm/:location',
		component: SearchResultPage,
		name: 'SearchResultPage',
	},
	{
		path: '/advanced-search',
		component: AdvancedSearchPage,
		name: 'AdvancedSearchPage',
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
