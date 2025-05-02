
type Page = {
  kind: 'page';
  readonly name: string;
  readonly query: string;
}

type Dir = {
  kind: 'dir';
  readonly name: string;
  readonly children: (Page | Dir)[];
}
