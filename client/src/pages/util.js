export const STATIC_VIEW_UI_SHAPE = [
	{
		header: 'Data Type',
		records: [
			{
				title: 'Record type',
				key: 'record_type',
				classNames:
					'mt-1 py-[.125rem] px-3 rounded-full bg-brand-wine/10 dark:bg-brand-wine dark:text-white w-fit small font-normal text-lg',
				component: 'Button',
				attributes: { intent: 'tertiary' },
				['data-test']: 'record-type-button',
			},
			{ title: 'Description', key: 'description' },
			{ title: 'Tags', key: 'tags' },
		],
	},
	{
		header: 'Access & format',
		records: [
			{
				title: 'Source URL',
				key: 'source_url',
				component: 'a',
				attributes: { target: '_blank', rel: 'noreferrer' },
				classNames: 'w-full inline-block truncate-text',
			},
			{
				key: 'source_url_cache',
				attributes: { intent: 'secondary' },
				component: 'PButton',
				classNames: 'flex gap-4 items-center',
				['data-test']: 'view-archives-button',
				text: 'View Archives',
				renderIf: 'last_cached',
				icon: 'fa-external-link',
			},
			{
				title: 'Last Archived',
				key: 'last_cached',
				isDate: true,
			},
			{
				title: 'ReadMe URL',
				key: 'readme_url',
				component: 'a',
				classNames: 'w-full inline-block truncate-text',
				attributes: { target: '_blank', rel: 'noreferrer' },
			},
			{ title: 'Access Type', key: 'access_type' },
			{
				title: 'Record Formats',
				key: 'record_format',
				classNames:
					'mt-1 py-[.125rem] px-3 rounded-full bg-slate-200 dark:bg-slate-600 w-fit small',
			},
			{ title: 'Detail Level', key: 'detail_level' },
			{ title: 'Size', key: 'size' },
			{ title: 'Access Notes', key: 'access_notes' },
			// records_not_online to be hidden
			// { title: "Records Not Online", key: "records_not_online" },
		],
	},
	{
		header: 'Agency',
		records: [
			{
				title: 'Name',
				key: 'agency_name',
				component: 'Button',
				classNames:
					'decoration-solid decoration-[6%] text-brand-gold  underline-offset-[5%] hover:brightness-85 small p-0 font-normal text-lg',
				attributes: { intent: 'tertiary' },
				['data-test']: 'agency-name-button',
			},
			{ title: 'State', key: 'state_iso' },
			{ title: 'County', key: 'county_name' },
			{ title: 'Municipality', key: 'municipality' },
			{ title: 'Agency Type', key: 'agency_type' },
			{ title: 'Jurisdiction Type', key: 'jurisdiction_type' },
		],
	},
	{
		header: 'Provenance',
		records: [
			{ title: 'Agency Supplied', key: 'agency_supplied' },
			{ title: 'Supplying Entity', key: 'supplying_entity' },
			{ title: 'Agency Originated', key: 'agency_originated' },
			{ title: 'Originating Entity', key: 'originating_entity' },
		],
	},
	{
		header: 'Coverage & retention',
		records: [
			{
				title: 'Coverage Start Date',
				key: 'coverage_start',
				isDate: true,
			},
			{ title: 'Coverage End Date', key: 'coverage_end', isDate: true },
			{
				title: 'Source Last Updated',
				key: 'source_last_updated',
				isDate: true,
			},
			{ title: 'Update Frequency', key: 'update_frequency' },
			{ title: 'Update Method', key: 'update_method' },
			{ title: 'Retention Schedule', key: 'retention_schedule' },
			{
				title: 'Number of Records Available',
				key: 'number_of_records_available',
			},
		],
	},
	{
		header: 'Data Source Meta',
		records: [
			{ title: 'Scraper URL', key: 'scraper_url' },
			{ title: 'Created', key: 'data_source_created', isDate: true },
			{ title: 'Agency ID', key: 'agency_id' },
			{ title: 'Data Source ID', key: 'data_source_id' },
		],
	},
];
